const isNumeric = (n) => {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

export { isNumeric };
