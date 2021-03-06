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

from epitopes import tantigen

def test_load_tcell():
    df = tantigen.load_tcell()
    assert df is not None
    assert len(df) > 0

def test_load_tcell_set():
    peptides = tantigen.load_tcell_set()
    assert peptides is not None
    assert len(peptides) > 0

def test_load_mhc():
    df = tantigen.load_mhc()
    assert df is not None
    assert len(df) > 0

def test_load_mhc_set():
    peptides = tantigen.load_mhc_set()
    assert peptides is not None
    assert len(peptides) > 0