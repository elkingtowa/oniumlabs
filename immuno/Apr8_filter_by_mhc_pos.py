# Copyright (c) 2014. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Try filtering the training set by MHC response = True, 
so that we're only predicting immunogenicity *given* MHC binding,
rather than predicting both together. 
"""
import numpy as np


import pandas as pd
import sklearn
import sklearn.cross_validation


from epitopes import \
    (cri_tumor_antigens, iedb, features,
    reduced_alphabet, reference,
    hiv_frahm)
from epitopes.peptide_vectorizer import PeptideVectorizer

import eval_dataset
from balanced_ensemble import BalancedEnsembleClassifier

cancer_peptides = cri_tumor_antigens.load_peptides(mhc_class = None)
non_immunogenic_hiv_peptides = \
    hiv_frahm.load_set(max_count = 0)
print "Positive validation set size: %d" % len(cancer_peptides)
print "Negative validation set size: %d" % len(non_immunogenic_hiv_peptides)


# sweet over filtering criteria and n-gram transformation
# parameters and for all parameter combos evaluate
# - cross-validation accuracy
# - cross-validation area under ROC curve
# - accuracy on validation set of cancer peptides


best_score = 0
best_params = None

param_count = 0
for assay in  ('cytokine release IFNg',):
    for alphabet in ('hp2', 'hp2', 'aromatic2', 'gbmr4', 'hp_vs_aromatic', 'sdm12', None):
        for max_ngram in (1,2,3,):#(1, 2, 3):
            for mhc_class in (1,2,None): #(1,2,None):
                if alphabet is None:
                    alphabet_dict = None
                    n_letters = 20
                else:
                    alphabet_dict = getattr(reduced_alphabet, alphabet)
                    n_letters = len(set(alphabet_dict.values()))
                n_features = 0
                for i in xrange(max_ngram):
                    n_features += n_letters ** (i+1)

                if n_features > 500:
                    continue
                else:
                    param_count += 1
                param_str =  \
                    "%d: Assay = '%s', ngram %s, alphabet %s, mhc_class %s" % \
                    (param_count, assay, max_ngram, alphabet, mhc_class)
                print param_str

                imm_pos, imm_neg = iedb.load_tcell_classes(
                    assay_group = assay,
                    human = True,
                    min_count = None, 
                    mhc_class = mhc_class)

                mhc_pos, _ = iedb.load_mhc_classes(
                    human = True, 
                    min_count = None, 
                    mhc_class = mhc_class)

                imm = list(mhc_pos.intersection(imm_pos))
                non = list(mhc_pos.intersection(imm_neg))

                vectorizer = PeptideVectorizer(
                    max_ngram = max_ngram,
                    reduced_alphabet = alphabet_dict)
                X = vectorizer.fit_transform(imm + non)
                Y = np.ones(len(X),dtype=int)
                Y[len(imm):] = 0

                print "Data shape", X.shape, "n_true", np.sum(Y)
                ensemble = BalancedEnsembleClassifier()

                accs = sklearn.cross_validation.cross_val_score(
                    ensemble, X, Y, cv = 5)
                acc = np.mean(accs)
                print "CV accuracy %0.4f (std %0.4f)" % \
                    (acc, np.std(accs))

                aucs = sklearn.cross_validation.cross_val_score(
                    ensemble, X, Y, cv = 5, scoring='roc_auc')
                auc = np.mean(aucs)
                print "CV AUC %0.4f (std %0.4f)" % \
                    (auc, np.std(aucs))

                ensemble.fit(X, Y)

                X_pos_test = vectorizer.transform(cancer_peptides)
                Y_pos_pred = ensemble.predict(X_pos_test)
                pos_acc = np.mean(Y_pos_pred)
                print "Tumor antigen accuracy %0.4f" % (pos_acc,)

                X_neg_test = vectorizer.transform(
                    non_immunogenic_hiv_peptides)
                Y_neg_pred = ensemble.predict(X_neg_test)
                neg_acc = 1.0 - np.mean(Y_neg_pred)
                print "Non-immunogenic accuracy %0.4f" % (neg_acc,)

                n_pos_pred = np.sum(Y_pos_pred)
                n_neg_pred = np.sum(Y_neg_pred)
                precision = n_pos_pred / float(n_pos_pred + n_neg_pred)
                recall = pos_acc
                f1_score = 2 * (precision * recall) / (precision + recall)
                print "F-1 score: %0.4f" % f1_score


                f_half_score = 1.25 * \
                    (precision * recall) / ((0.25 * precision) + recall)

                print "F-0.5 score: %0.4f" % f_half_score

                print "---"
                print
		
		if f_half_score > best_score:
			best_score = f_half_score
			best_params = param_str

print "BEST"
print "Score", best_score
print "Params", best_params
