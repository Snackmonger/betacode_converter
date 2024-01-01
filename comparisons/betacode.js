/**
 * Originally from https://www.translatum.gr/converter/beta-code.htm. Used here for educational purposes.
 */


(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
(function () {
'use strict';

var beta_code_to_unicode = require('./vendor/beta-code-json/beta_code_to_unicode.json');
var unicode_to_beta_code = require('./vendor/beta-code-json/unicode_to_beta_code.json');
var max_beta_code_character_length = _longestKeyLength(beta_code_to_unicode);

function greekToBetaCode (greek) {
  var greek_characters = _normalize(greek).split('');
  var beta_code_characters = [];
  var current_character, ii;

  for (ii = 0; ii < greek_characters.length; ii++) {
    current_character = greek_characters[ii];

    if (unicode_to_beta_code.hasOwnProperty(current_character)) {
      beta_code_characters.push(unicode_to_beta_code[current_character]);
    } else {
      beta_code_characters.push(current_character);
    }
  }

  return beta_code_characters.join('');
}

function betaCodeToGreek (beta_code) {
  var beta_code_characters = _normalize(beta_code).split('');
  var greek_characters = [];
  var start = 0;
  var end, slice, new_start, current_character, max_length;

  while (start <= beta_code_characters.length) {
    current_character = beta_code_characters[start];
    new_start = start + 1;
    max_length = _min(beta_code_characters.length, start + max_beta_code_character_length);

    // match the longest possible substring that's valid beta code, from left to right
    // for example 'e)' is valid beta code (ἐ) but 'e)/' is also valid beta code (ἕ)
    // the string 'e)/' should be interpreted as 'e)/' and not as 'e)' + '/'
    for (end = new_start; end <= max_length; end++) {
      slice = beta_code_characters.slice(start, end).join('');

      if (beta_code_to_unicode.hasOwnProperty(slice)) {
        current_character = beta_code_to_unicode[slice];
        new_start = end;
      }
    }

    greek_characters.push(current_character);
    start = new_start;
  }

  return _sigmaToEndOfWordSigma(greek_characters.join(''));
}

module.exports = {
  greekToBetaCode: greekToBetaCode,
  betaCodeToGreek: betaCodeToGreek
};

if (typeof window !== 'undefined') {
  window.greekToBetaCode = greekToBetaCode;
  window.betaCodeToGreek = betaCodeToGreek;
}

function _longestKeyLength (obj) {
  var key;
  var length = 0;

  for (key in obj) {
    if (obj.hasOwnProperty(key)) {
      if (key.length > length) {
        length = key.length;
      }
    }
  }

  return length;
}

// this function replaces σ with ς when:
//   - at the end of a line
//   - followed by whitespace
//   - followed by a punctuation character
// REGEX NOTE: word boundary \b doesn't work well with unicode
function _sigmaToEndOfWordSigma (string) {
  return string.replace(/σ(?=[,.:;·\s]|$)/g, 'ς');
}

function _min (a, b) {
  return a < b ? a : b;
}

function _normalize (string) {
  if (string.normalize) {
    return string.normalize();
  }

  return string;
}
})();

},{"./vendor/beta-code-json/beta_code_to_unicode.json":2,"./vendor/beta-code-json/unicode_to_beta_code.json":3}],2:[function(require,module,exports){
module.exports={
  "*v": "Ϝ",
  "v": "ϝ",
  "a": "α",
  "*a": "Α",
  "b": "β",
  "*b": "Β",
  "g": "γ",
  "*g": "Γ",
  "d": "δ",
  "*d": "Δ",
  "e": "ε",
  "*e": "Ε",
  "z": "ζ",
  "*z": "Ζ",
  "h": "η",
  "*h": "Η",
  "q": "θ",
  "*q": "Θ",
  "i": "ι",
  "*i": "Ι",
  "k": "κ",
  "*k": "Κ",
  "l": "λ",
  "*l": "Λ",
  "m": "μ",
  "*m": "Μ",
  "n": "ν",
  "*n": "Ν",
  "c": "ξ",
  "*c": "Ξ",
  "o": "ο",
  "*o": "Ο",
  "p": "π",
  "*p": "Π",
  "r": "ρ",
  "r)": "ῤ",
  "r(": "ῥ",
  "*r": "Ρ",
  "*(r": "Ῥ",
  "s": "σ",
  "*s": "Σ",
  "s1": "σ",
  "*s1": "Σ",
  "s2": "ς",
  "*s2": "Σ",
  "j": "ς",
  "*j": "Σ",
  "s3": "ϲ",
  "*s3": "Ϲ",
  "t": "τ",
  "*t": "Τ",
  "u": "υ",
  "*u": "Υ",
  "f": "φ",
  "*f": "Φ",
  "x": "χ",
  "*x": "Χ",
  "y": "ψ",
  "*y": "Ψ",
  "w": "ω",
  "*w": "Ω",
  ".": ".",
  ",": ",",
  ":": "·",
  ";": ";",
  "-": "-",
  "_": "—",
  ")": "ʼ",
  "(": "ʽ",
  "/": " ́",
  "=": " ͂",
  "\\": "`",
  "+": " ̈",
  "a)": "ἀ",
  "a(": "ἁ",
  "a/": "ά",
  "a\\": "ὰ",
  "a=": "ᾶ",
  "a|": "ᾳ",
  "a)|": "ᾀ",
  "a(|": "ᾁ",
  "a/|": "ᾴ",
  "a\\|": "ᾲ",
  "a=|": "ᾷ",
  "a)/": "ἄ",
  "a(/": "ἅ",
  "a)\\": "ἂ",
  "a(\\": "ἃ",
  "a)=": "ἆ",
  "a(=": "ἇ",
  "a)/|": "ᾄ",
  "a(/|": "ᾅ",
  "a(\\|": "ᾃ",
  "a)=|": "ᾆ",
  "a(=|": "ᾇ",
  "*)a": "Ἀ",
  "*(a": "Ἁ",
  "*/a": "Ά",
  "*\\a": "Ὰ",
  "*|a": "ᾼ",
  "*)|a": "ᾈ",
  "*(|a": "ᾉ",
  "*)/a": "Ἄ",
  "*(/a": "Ἅ",
  "*(\\a": "Ἃ",
  "*)=a": "Ἆ",
  "*(=a": "Ἇ",
  "*)/|a": "ᾌ",
  "*(/|a": "ᾍ",
  "*(\\|a": "ᾋ",
  "*)=|a": "ᾎ",
  "*(=|a": "ᾏ",
  "e)": "ἐ",
  "e(": "ἑ",
  "e/": "έ",
  "e\\": "ὲ",
  "e)\\": "ἒ",
  "e(\\": "ἓ",
  "e)/": "ἔ",
  "e(/": "ἕ",
  "*)e": "Ἐ",
  "*(e": "Ἑ",
  "*/e": "Έ",
  "*\\e": "Ὲ",
  "*)\\e": "Ἒ",
  "*(\\e": "Ἓ",
  "*)/e": "Ἔ",
  "*(/e": "Ἕ",
  "h)": "ἠ",
  "h(": "ἡ",
  "h/": "ή",
  "h\\": "ὴ",
  "h=": "ῆ",
  "h|": "ῃ",
  "h)|": "ᾐ",
  "h(|": "ᾑ",
  "h/|": "ῄ",
  "h\\|": "ῂ",
  "h=|": "ῇ",
  "h)/": "ἤ",
  "h(/": "ἥ",
  "h(\\": "ἣ",
  "h)=": "ἦ",
  "h(=": "ἧ",
  "h)/|": "ᾔ",
  "h(/|": "ᾕ",
  "h(\\|": "ᾓ",
  "h)=|": "ᾖ",
  "h(=|": "ᾗ",
  "*)h": "Ἠ",
  "*(h": "Ἡ",
  "*/h": "Ή",
  "*\\h": "Ὴ",
  "*|h": "ῌ",
  "*)|h": "ᾘ",
  "*(|h": "ᾙ",
  "*)/h": "Ἤ",
  "*(/h": "Ἥ",
  "*(\\h": "Ἣ",
  "*)=h": "Ἦ",
  "*(=h": "Ἧ",
  "*)/|h": "ᾜ",
  "*(/|h": "ᾝ",
  "*(\\|h": "ᾛ",
  "*)=|h": "ᾞ",
  "*(=|h": "ᾟ",
  "i)": "ἰ",
  "i(": "ἱ",
  "i/": "ί",
  "i\\": "ὶ",
  "i=": "ῖ",
  "i+": "ϊ",
  "i)\\": "ἲ",
  "i(\\": "ἳ",
  "i)/": "ἴ",
  "i(/": "ἵ",
  "i)=": "ἶ",
  "i(=": "ἷ",
  "i/+": "ΐ",
  "i\\+": "ῒ",
  "i=+": "ῗ",
  "*)i": "Ἰ",
  "*(i": "Ἱ",
  "*/i": "Ί",
  "*\\i": "Ὶ",
  "*+i": "Ϊ",
  "*)\\i": "Ἲ",
  "*(\\i": "Ἳ",
  "*)/i": "Ἴ",
  "*(/i": "Ἵ",
  "*)=i": "Ἶ",
  "*(=i": "Ἷ",
  "o)": "ὀ",
  "o(": "ὁ",
  "o/": "ό",
  "o\\": "ὸ",
  "o)\\": "ὂ",
  "o(\\": "ὃ",
  "o)/": "ὄ",
  "o(/": "ὅ",
  "*)o": "Ὀ",
  "*(o": "Ὁ",
  "*/o": "Ό",
  "*\\o": "Ὸ",
  "*)\\o": "Ὂ",
  "*(\\o": "Ὃ",
  "*)/o": "Ὄ",
  "*(/o": "Ὅ",
  "u)": "ὐ",
  "u(": "ὑ",
  "u/": "ύ",
  "u\\": "ὺ",
  "u=": "ῦ",
  "u+": "ϋ",
  "u)\\": "ὒ",
  "u(\\": "ὓ",
  "u)/": "ὔ",
  "u(/": "ὕ",
  "u)=": "ὖ",
  "u(=": "ὗ",
  "u/+": "ΰ",
  "u\\+": "ῢ",
  "u=+": "ῧ",
  "*(u": "Ὑ",
  "*/u": "Ύ",
  "*\\u": "Ὺ",
  "*+u": "Ϋ",
  "*(\\u": "Ὓ",
  "*(/u": "Ὕ",
  "*(=u": "Ὗ",
  "w)": "ὠ",
  "w(": "ὡ",
  "w/": "ώ",
  "w\\": "ὼ",
  "w=": "ῶ",
  "w|": "ῳ",
  "w)|": "ᾠ",
  "w(|": "ᾡ",
  "w/|": "ῴ",
  "w\\|": "ῲ",
  "w=|": "ῷ",
  "w)/": "ὤ",
  "w(/": "ὥ",
  "w(\\": "ὣ",
  "w)=": "ὦ",
  "w(=": "ὧ",
  "w)/|": "ᾤ",
  "w(/|": "ᾥ",
  "w(\\|": "ᾣ",
  "w)=|": "ᾦ",
  "w(=|": "ᾧ",
  "*)w": "Ὠ",
  "*(w": "Ὡ",
  "*/w": "Ώ",
  "*\\w": "Ὼ",
  "*|w": "ῼ",
  "*)|w": "ᾨ",
  "*(|w": "ᾩ",
  "*)/w": "Ὤ",
  "*(/w": "Ὥ",
  "*(\\w": "Ὣ",
  "*)=w": "Ὦ",
  "*(=w": "Ὧ",
  "*)/|w": "ᾬ",
  "*(/|w": "ᾭ",
  "*(\\|w": "ᾫ",
  "*)=|w": "ᾮ",
  "*(=|w": "ᾯ",
  "A": "α",
  "*A": "Α",
  "B": "β",
  "*B": "Β",
  "G": "γ",
  "*G": "Γ",
  "D": "δ",
  "*D": "Δ",
  "E": "ε",
  "*E": "Ε",
  "Z": "ζ",
  "*Z": "Ζ",
  "H": "η",
  "*H": "Η",
  "Q": "θ",
  "*Q": "Θ",
  "I": "ι",
  "*I": "Ι",
  "K": "κ",
  "*K": "Κ",
  "L": "λ",
  "*L": "Λ",
  "M": "μ",
  "*M": "Μ",
  "N": "ν",
  "*N": "Ν",
  "C": "ξ",
  "*C": "Ξ",
  "O": "ο",
  "*O": "Ο",
  "P": "π",
  "*P": "Π",
  "R": "ρ",
  "R)": "ῤ",
  "R(": "ῥ",
  "*R": "Ρ",
  "*(R": "Ῥ",
  "S": "σ",
  "*S": "Σ",
  "S1": "σ",
  "*S1": "Σ",
  "S2": "ς",
  "*S2": "Σ",
  "J": "ς",
  "*J": "Σ",
  "S3": "ϲ",
  "*S3": "Ϲ",
  "T": "τ",
  "*T": "Τ",
  "U": "υ",
  "*U": "Υ",
  "F": "φ",
  "*F": "Φ",
  "X": "χ",
  "*X": "Χ",
  "Y": "ψ",
  "*Y": "Ψ",
  "W": "ω",
  "*W": "Ω",
  "A)": "ἀ",
  "A(": "ἁ",
  "A/": "ά",
  "A\\": "ὰ",
  "A=": "ᾶ",
  "A|": "ᾳ",
  "A)|": "ᾀ",
  "A(|": "ᾁ",
  "A/|": "ᾴ",
  "A\\|": "ᾲ",
  "A=|": "ᾷ",
  "A)/": "ἄ",
  "A(/": "ἅ",
  "A)\\": "ἂ",
  "A(\\": "ἃ",
  "A)=": "ἆ",
  "A(=": "ἇ",
  "A)/|": "ᾄ",
  "A(/|": "ᾅ",
  "A(\\|": "ᾃ",
  "A)=|": "ᾆ",
  "A(=|": "ᾇ",
  "*)A": "Ἀ",
  "*(A": "Ἁ",
  "*/A": "Ά",
  "*\\A": "Ὰ",
  "*|A": "ᾼ",
  "*)|A": "ᾈ",
  "*(|A": "ᾉ",
  "*)/A": "Ἄ",
  "*(/A": "Ἅ",
  "*(\\A": "Ἃ",
  "*)=A": "Ἆ",
  "*(=A": "Ἇ",
  "*)/|A": "ᾌ",
  "*(/|A": "ᾍ",
  "*(\\|A": "ᾋ",
  "*)=|A": "ᾎ",
  "*(=|A": "ᾏ",
  "E)": "ἐ",
  "E(": "ἑ",
  "E/": "έ",
  "E\\": "ὲ",
  "E)\\": "ἒ",
  "E(\\": "ἓ",
  "E)/": "ἔ",
  "E(/": "ἕ",
  "*)E": "Ἐ",
  "*(E": "Ἑ",
  "*/E": "Έ",
  "*\\E": "Ὲ",
  "*)\\E": "Ἒ",
  "*(\\E": "Ἓ",
  "*)/E": "Ἔ",
  "*(/E": "Ἕ",
  "H)": "ἠ",
  "H(": "ἡ",
  "H/": "ή",
  "H\\": "ὴ",
  "H=": "ῆ",
  "H|": "ῃ",
  "H)|": "ᾐ",
  "H(|": "ᾑ",
  "H/|": "ῄ",
  "H\\|": "ῂ",
  "H=|": "ῇ",
  "H)/": "ἤ",
  "H(/": "ἥ",
  "H(\\": "ἣ",
  "H)=": "ἦ",
  "H(=": "ἧ",
  "H)/|": "ᾔ",
  "H(/|": "ᾕ",
  "H(\\|": "ᾓ",
  "H)=|": "ᾖ",
  "H(=|": "ᾗ",
  "*)H": "Ἠ",
  "*(H": "Ἡ",
  "*/H": "Ή",
  "*\\H": "Ὴ",
  "*|H": "ῌ",
  "*)|H": "ᾘ",
  "*(|H": "ᾙ",
  "*)/H": "Ἤ",
  "*(/H": "Ἥ",
  "*(\\H": "Ἣ",
  "*)=H": "Ἦ",
  "*(=H": "Ἧ",
  "*)/|H": "ᾜ",
  "*(/|H": "ᾝ",
  "*(\\|H": "ᾛ",
  "*)=|H": "ᾞ",
  "*(=|H": "ᾟ",
  "I)": "ἰ",
  "I(": "ἱ",
  "I/": "ί",
  "I\\": "ὶ",
  "I=": "ῖ",
  "I+": "ϊ",
  "I)\\": "ἲ",
  "I(\\": "ἳ",
  "I)/": "ἴ",
  "I(/": "ἵ",
  "I)=": "ἶ",
  "I(=": "ἷ",
  "I/+": "ΐ",
  "I\\+": "ῒ",
  "I=+": "ῗ",
  "*)I": "Ἰ",
  "*(I": "Ἱ",
  "*/I": "Ί",
  "*\\I": "Ὶ",
  "*+I": "Ϊ",
  "*)\\I": "Ἲ",
  "*(\\I": "Ἳ",
  "*)/I": "Ἴ",
  "*(/I": "Ἵ",
  "*)=I": "Ἶ",
  "*(=I": "Ἷ",
  "O)": "ὀ",
  "O(": "ὁ",
  "O/": "ό",
  "O\\": "ὸ",
  "O)\\": "ὂ",
  "O(\\": "ὃ",
  "O)/": "ὄ",
  "O(/": "ὅ",
  "*)O": "Ὀ",
  "*(O": "Ὁ",
  "*/O": "Ό",
  "*\\O": "Ὸ",
  "*)\\O": "Ὂ",
  "*(\\O": "Ὃ",
  "*)/O": "Ὄ",
  "*(/O": "Ὅ",
  "U)": "ὐ",
  "U(": "ὑ",
  "U/": "ύ",
  "U\\": "ὺ",
  "U=": "ῦ",
  "U+": "ϋ",
  "U)\\": "ὒ",
  "U(\\": "ὓ",
  "U)/": "ὔ",
  "U(/": "ὕ",
  "U)=": "ὖ",
  "U(=": "ὗ",
  "U/+": "ΰ",
  "U\\+": "ῢ",
  "U=+": "ῧ",
  "*(U": "Ὑ",
  "*/U": "Ύ",
  "*\\U": "Ὺ",
  "*+U": "Ϋ",
  "*(\\U": "Ὓ",
  "*(/U": "Ὕ",
  "*(=U": "Ὗ",
  "W)": "ὠ",
  "W(": "ὡ",
  "W/": "ώ",
  "W\\": "ὼ",
  "W=": "ῶ",
  "W|": "ῳ",
  "W)|": "ᾠ",
  "W(|": "ᾡ",
  "W/|": "ῴ",
  "W\\|": "ῲ",
  "W=|": "ῷ",
  "W)/": "ὤ",
  "W(/": "ὥ",
  "W(\\": "ὣ",
  "W)=": "ὦ",
  "W(=": "ὧ",
  "W)/|": "ᾤ",
  "W(/|": "ᾥ",
  "W(\\|": "ᾣ",
  "W)=|": "ᾦ",
  "W(=|": "ᾧ",
  "*)W": "Ὠ",
  "*(W": "Ὡ",
  "*/W": "Ώ",
  "*\\W": "Ὼ",
  "*|W": "ῼ",
  "*)|W": "ᾨ",
  "*(|W": "ᾩ",
  "*)/W": "Ὤ",
  "*(/W": "Ὥ",
  "*(\\W": "Ὣ",
  "*)=W": "Ὦ",
  "*(=W": "Ὧ",
  "*)/|W": "ᾬ",
  "*(/|W": "ᾭ",
  "*(\\|W": "ᾫ",
  "*)=|W": "ᾮ",
  "*(=|W": "ᾯ",
  "#": "ʹ"
}

},{}],3:[function(require,module,exports){
module.exports={
  "Ϝ": "*v",
  "ϝ": "v",
  "α": "a",
  "Α": "*a",
  "β": "b",
  "Β": "*b",
  "γ": "g",
  "Γ": "*g",
  "δ": "d",
  "Δ": "*d",
  "ε": "e",
  "Ε": "*e",
  "ζ": "z",
  "Ζ": "*z",
  "η": "h",
  "Η": "*h",
  "θ": "q",
  "Θ": "*q",
  "ι": "i",
  "Ι": "*i",
  "κ": "k",
  "Κ": "*k",
  "λ": "l",
  "Λ": "*l",
  "μ": "m",
  "Μ": "*m",
  "ν": "n",
  "Ν": "*n",
  "ξ": "c",
  "Ξ": "*c",
  "ο": "o",
  "Ο": "*o",
  "π": "p",
  "Π": "*p",
  "ρ": "r",
  "ῤ": "r)",
  "ῥ": "r(",
  "Ρ": "*r",
  "Ῥ": "*(r",
  "ς": "s",
  "ϲ": "s3",
  "Ϲ": "*s3",
  "σ": "s",
  "Σ": "*s",
  "τ": "t",
  "Τ": "*t",
  "υ": "u",
  "Υ": "*u",
  "φ": "f",
  "Φ": "*f",
  "χ": "x",
  "Χ": "*x",
  "ψ": "y",
  "Ψ": "*y",
  "ω": "w",
  "Ω": "*w",
  ".": ".",
  ",": ",",
  "·": ":",
  "·": ":",
  ";": ";",
  "-": "-",
  "—": "_",
  "ʼ": ")",
  "ʽ": "(",
  " ́": "/",
  " ͂": "=",
  "`": "\\",
  " ̈": "+",
  "ἀ": "a)",
  "ἁ": "a(",
  "ά": "a/",
  "ὰ": "a\\",
  "ᾶ": "a=",
  "ᾳ": "a|",
  "ᾀ": "a)|",
  "ᾁ": "a(|",
  "ᾴ": "a/|",
  "ᾲ": "a\\|",
  "ᾷ": "a=|",
  "ἄ": "a)/",
  "ἅ": "a(/",
  "ἂ": "a)\\",
  "ἃ": "a(\\",
  "ἆ": "a)=",
  "ἇ": "a(=",
  "ᾄ": "a)/|",
  "ᾅ": "a(/|",
  "ᾂ": "a(\\|",
  "ᾃ": "a(\\|",
  "ᾆ": "a)=|",
  "ᾇ": "a(=|",
  "Ἀ": "*)a",
  "Ἁ": "*(a",
  "Ά": "*/a",
  "Ὰ": "*\\a",
  "ᾼ": "*|a",
  "ᾈ": "*)|a",
  "ᾉ": "*(|a",
  "Ἄ": "*)/a",
  "Ἅ": "*(/a",
  "Ἂ": "*(\\a",
  "Ἃ": "*(\\a",
  "Ἆ": "*)=a",
  "Ἇ": "*(=a",
  "ᾌ": "*)/|a",
  "ᾍ": "*(/|a",
  "ᾊ": "*(\\|a",
  "ᾋ": "*(\\|a",
  "ᾎ": "*)=|a",
  "ᾏ": "*(=|a",
  "ἐ": "e)",
  "ἑ": "e(",
  "έ": "e/",
  "ὲ": "e\\",
  "ἒ": "e)\\",
  "ἓ": "e(\\",
  "ἔ": "e)/",
  "ἕ": "e(/",
  "Ἐ": "*)e",
  "Ἑ": "*(e",
  "Έ": "*/e",
  "Ὲ": "*\\e",
  "Ἒ": "*)\\e",
  "Ἓ": "*(\\e",
  "Ἔ": "*)/e",
  "Ἕ": "*(/e",
  "ἠ": "h)",
  "ἡ": "h(",
  "ή": "h/",
  "ὴ": "h\\",
  "ῆ": "h=",
  "ῃ": "h|",
  "ᾐ": "h)|",
  "ᾑ": "h(|",
  "ῄ": "h/|",
  "ῂ": "h\\|",
  "ῇ": "h=|",
  "ἤ": "h)/",
  "ἥ": "h(/",
  "ἢ": "h(\\",
  "ἣ": "h(\\",
  "ἦ": "h)=",
  "ἧ": "h(=",
  "ᾔ": "h)/|",
  "ᾕ": "h(/|",
  "ᾒ": "h(\\|",
  "ᾓ": "h(\\|",
  "ᾖ": "h)=|",
  "ᾗ": "h(=|",
  "Ἠ": "*)h",
  "Ἡ": "*(h",
  "Ή": "*/h",
  "Ὴ": "*\\h",
  "ῌ": "*|h",
  "ᾘ": "*)|h",
  "ᾙ": "*(|h",
  "Ἤ": "*)/h",
  "Ἥ": "*(/h",
  "Ἢ": "*(\\h",
  "Ἣ": "*(\\h",
  "Ἦ": "*)=h",
  "Ἧ": "*(=h",
  "ᾜ": "*)/|h",
  "ᾝ": "*(/|h",
  "ᾚ": "*(\\|h",
  "ᾛ": "*(\\|h",
  "ᾞ": "*)=|h",
  "ᾟ": "*(=|h",
  "ἰ": "i)",
  "ἱ": "i(",
  "ί": "i/",
  "ὶ": "i\\",
  "ῖ": "i=",
  "ϊ": "i+",
  "ἲ": "i)\\",
  "ἳ": "i(\\",
  "ἴ": "i)/",
  "ἵ": "i(/",
  "ἶ": "i)=",
  "ἷ": "i(=",
  "ΐ": "i/+",
  "ῒ": "i\\+",
  "ῗ": "i=+",
  "Ἰ": "*)i",
  "Ἱ": "*(i",
  "Ί": "*/i",
  "Ὶ": "*\\i",
  "Ϊ": "*+i",
  "Ἲ": "*)\\i",
  "Ἳ": "*(\\i",
  "Ἴ": "*)/i",
  "Ἵ": "*(/i",
  "Ἶ": "*)=i",
  "Ἷ": "*(=i",
  "ὀ": "o)",
  "ὁ": "o(",
  "ό": "o/",
  "ὸ": "o\\",
  "ὂ": "o)\\",
  "ὃ": "o(\\",
  "ὄ": "o)/",
  "ὅ": "o(/",
  "Ὀ": "*)o",
  "Ὁ": "*(o",
  "Ό": "*/o",
  "Ὸ": "*\\o",
  "Ὂ": "*)\\o",
  "Ὃ": "*(\\o",
  "Ὄ": "*)/o",
  "Ὅ": "*(/o",
  "ὐ": "u)",
  "ὑ": "u(",
  "ύ": "u/",
  "ὺ": "u\\",
  "ῦ": "u=",
  "ϋ": "u+",
  "ὒ": "u)\\",
  "ὓ": "u(\\",
  "ὔ": "u)/",
  "ὕ": "u(/",
  "ὖ": "u)=",
  "ὗ": "u(=",
  "ΰ": "u/+",
  "ῢ": "u\\+",
  "ῧ": "u=+",
  "Ὑ": "*(u",
  "Ύ": "*/u",
  "Ὺ": "*\\u",
  "Ϋ": "*+u",
  "Ὓ": "*(\\u",
  "Ὕ": "*(/u",
  "Ὗ": "*(=u",
  "ὠ": "w)",
  "ὡ": "w(",
  "ώ": "w/",
  "ὼ": "w\\",
  "ῶ": "w=",
  "ῳ": "w|",
  "ᾠ": "w)|",
  "ᾡ": "w(|",
  "ῴ": "w/|",
  "ῲ": "w\\|",
  "ῷ": "w=|",
  "ὤ": "w)/",
  "ὥ": "w(/",
  "ὢ": "w(\\",
  "ὣ": "w(\\",
  "ὦ": "w)=",
  "ὧ": "w(=",
  "ᾤ": "w)/|",
  "ᾥ": "w(/|",
  "ᾢ": "w(\\|",
  "ᾣ": "w(\\|",
  "ᾦ": "w)=|",
  "ᾧ": "w(=|",
  "Ὠ": "*)w",
  "Ὡ": "*(w",
  "Ώ": "*/w",
  "Ὼ": "*\\w",
  "ῼ": "*|w",
  "ᾨ": "*)|w",
  "ᾩ": "*(|w",
  "Ὤ": "*)/w",
  "Ὥ": "*(/w",
  "Ὢ": "*(\\w",
  "Ὣ": "*(\\w",
  "Ὦ": "*)=w",
  "Ὧ": "*(=w",
  "ᾬ": "*)/|w",
  "ᾭ": "*(/|w",
  "ᾪ": "*(\\|w",
  "ᾫ": "*(\\|w",
  "ᾮ": "*)=|w",
  "ᾯ": "*(=|w",
  "᾽": "'",
  "ʹ": "#"
}

},{}]},{},[1]);
