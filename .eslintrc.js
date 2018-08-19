module.exports = {
  env: {
    browser: false,
    node: true,
    jest: true,
    es6: true
  },
  parserOptions: { ecmaVersion: 8 },
  extends: ["airbnb-base", "prettier"],
  rules: {
    "global-require": 0,
    "import/no-dynamic-require": 0,
    "no-use-before-define": 0,
    "no-console": 0,
    "react/jsx-filename-extension": 0,
    "react/prop-types": 0,
    "import/prefer-default-export": 0,
    "no-underscore-dangle": 0,
    "no-else-return": 0
  }
}
