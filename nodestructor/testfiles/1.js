const obj1 = {};
obj1.__proto__.x = 1;
console.log(obj1.x === 1); // true
const obj2 = {};
console.log(obj2.x === 1); // true
