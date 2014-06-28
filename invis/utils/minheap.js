/* A simple binary min-heap serving as a priority queue
   - takes an array as the input, with elements having a key property
   - elements will look like this:
        {
            key: "... key property ...",
            value: "... element content ..."
        }
    - provides insert(), min(), extractMin() and heapify()
    - example usage (e.g. via the Firebug or Chromium console):
        var x = {foo: 20, hui: "bla"};
        var a = new BinaryMinHeap([x,{foo:3},{foo:10},{foo:20},{foo:30},{foo:6},{foo:1},{foo:3}],"foo");
        console.log(a.extractMin());
        console.log(a.extractMin());
        x.foo = 0; // update key
        a.heapify(); // call this always after having a key updated
        console.log(a.extractMin());
        console.log(a.extractMin());
    - can also be used on a simple array, like [9,7,8,5]

  */
function BinaryMinHeap(array, key) {

  // Binary tree stored in an array
  this.tree_ = [];
  this.key_  = key || 'key';

  // insert the input elements
  for(var i in array)
    this.insert(array[i]);

}


//Helper function to swap elements with the smaller of their children
//as long as there is one
BinaryMinHeap.prototype.bubbleDown = function(i) {

  var l = this.left(i);
  var r = this.right(i);

  /* as long as there are smaller children */
  while(this.tree_[l] && (this.tree_[i][this.key_] > this.tree_[l][this.key_])||
        this.tree_[r] && (this.tree_[i][this.key_] > this.tree_[r][this.key_])) {

    /* find smaller child */
    var child = this.tree_[l] ? this.tree_[r] ? this.tree_[l][this.key_] > this.tree_[r][this.key_] ? r : l : l : l;

    /* swap with smaller child with current element */
    this.tree_[i] = this.tree_.splice(child, 1, this.tree_[i])[0];

    /* go up one level */
    i = child;
    l = this.left(i);
    r = this.right(i);
  }
}


/* Helper function to swap elements with their parent
   as long as the parent is bigger */
BinaryMinHeap.prototype.bubbleUp= function(i) {
  var p = this.parent(i);
  while((p >= 0) && (this.tree_[i][this.key_] < this.tree_[p][this.key_])) {

    /* swap with parent */
    this.tree_[i] = this.tree_.splice(p, 1, this.tree_[i])[0];

    /* go up one level */
    i = p;
    p = this.parent(i);
  }

}



/* Insert a new element with respect to the heap property
   1. Insert the element at the end
   2. Bubble it up until it is smaller than its parent */
BinaryMinHeap.prototype.insert = function(element) {

	//   console.log("pushing element:",element);
	//   console.log("element[this.key_]", element[this.key_]);

  /* make sure there's a this.key_ property */
  if(element[this.key_] == undefined)  element = {key:element};

  /* insert element at the end */
  this.tree_.push(element);

  /* bubble up the element */
  this.bubbleUp(this.tree_.length - 1);
}


/* Only show us the minimum */
BinaryMinHeap.prototype.min = function() {
  return this.tree_.length == 0 ? undefined : this.tree_[0];
};


  /* Return and remove the minimum
     1. Take the root as the minimum that we are looking for
     2. Move the last element to the root (thereby deleting the root)
     3. Compare the new root with both of its children, swap it with the
     smaller child and then check again from there (bubble down)
     */
  BinaryMinHeap.prototype.extractMin = function() {

    var result = this.min();

    /* move the last element to the root or empty the tree completely */
    /* bubble down the new root if necessary */
    (this.tree_.length == 1) && (this.tree_ = []) || (this.tree_[0] = this.tree_.pop()) && this.bubbleDown(0);

  return result;
}


BinaryMinHeap.prototype.heapify = function() {

  for(var start = Math.floor((this.tree_.length - 2) / 2); start >= 0; start--) {
    this.bubbleDown(start);
  }
}

/* Calculate the index of the parent or a child */
BinaryMinHeap.prototype.parent = function(index) { return ~~((index - 1)/2); }
BinaryMinHeap.prototype.right = function(index) { return 2 * index + 2; }
BinaryMinHeap.prototype.left= function(index) { return 2 * index + 1;}

