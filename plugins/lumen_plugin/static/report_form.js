/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 2);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/report_form.js":
/*!*******************************!*\
  !*** ./src/js/report_form.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("(function reportFormSetUp() {\n  var scheduleTypeInput = document.getElementById(\"schedule_type\");\n  var scheduleWeekDayRow = document.getElementById(\"schedule_week_day\").closest(\"tr\");\n  var scheduleTime = document.getElementById(\"schedule_time\").closest(\"tr\");\n  var scheduleCustomRow = document.getElementById(\"schedule_custom\").closest(\"tr\"); // detect currently selected schedule type and\n  // display appropriate fields\n\n  configureScheduleUI(scheduleTypeInput.value);\n  $(scheduleTypeInput).on(\"change\", function ($event) {\n    configureScheduleUI($event.target.value);\n  });\n  /**\n   * Configure schedule UI according to the schedule type\n   *\n   * @param {string} scheduleType type of the schedule\n   */\n\n  function configureScheduleUI(scheduleType) {\n    switch (scheduleType) {\n      case \"daily\":\n        enableDailySchedule();\n        break;\n\n      case \"weekly\":\n        enableWeeklySchedule();\n        break;\n\n      case \"custom\":\n        enableCustomSchedule();\n\n      default:\n        break;\n    }\n  }\n  /**\n   * Display daily schedule fields\n   */\n\n\n  function enableDailySchedule() {\n    scheduleTime.hidden = false;\n    scheduleWeekDayRow.hidden = true;\n    scheduleCustomRow.hidden = true;\n  }\n  /**\n   * Display weekly schedule fields\n   */\n\n\n  function enableWeeklySchedule() {\n    scheduleTime.hidden = false;\n    scheduleWeekDayRow.hidden = false;\n    scheduleCustomRow.hidden = true;\n  }\n  /**\n   * Display custom schedule fields\n   */\n\n\n  function enableCustomSchedule() {\n    scheduleTime.hidden = true;\n    scheduleWeekDayRow.hidden = true;\n    scheduleCustomRow.hidden = false;\n  }\n})();\n\n//# sourceURL=webpack:///./src/js/report_form.js?");

/***/ }),

/***/ 2:
/*!*************************************!*\
  !*** multi ./src/js/report_form.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("module.exports = __webpack_require__(/*! ./src/js/report_form.js */\"./src/js/report_form.js\");\n\n\n//# sourceURL=webpack:///multi_./src/js/report_form.js?");

/***/ })

/******/ });