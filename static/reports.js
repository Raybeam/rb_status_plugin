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
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/reports.js":
/*!***************************!*\
  !*** ./src/js/reports.js ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports) {

/*global postAsForm */
// expose lumen API
window.lumen = {
  confirmDeleteReport: confirmDeleteReport,
  triggerReportStartPause: triggerReportStartPause
};
/**
 * Delete report.
 * Ask user for confirmation prior to sending a request.
 *
 * @param {HTMLElement} link html element the function is called on
 */
// eslint-disable-next-line no-unused-vars

function confirmDeleteReport(link) {
  var reportName = link.dataset.reportName;
  var answer = confirm("Are you sure you want to delete \"".concat(reportName, "\" report?"));

  if (answer) {
    postAsForm(link.href, {
      report_name: reportName
    });
  }

  return false;
}
/**
 * Start/Pause report trigger handler.
 *
 * @param {HTMLElement} input html input element the function is called on
 */


function triggerReportStartPause(input) {
  var url = input.dataset.pauseUrl;
  var reportName = encodeURIComponent(input.dataset.reportName);
  var isPaused = input.checked;
  url = "".concat(url, "?report_name=").concat(reportName, "&is_paused=").concat(isPaused);
  var data = new FormData();
  data.append("csrf_token", typeof csrfToken === "undefined" || csrfToken === null ? CSRF : csrfToken);
  fetch(url, {
    method: "POST",
    body: data
  }).then(function (response) {
    if (!response.ok) {
      $(input).data("bs.toggle").off(!isPaused);
    }
  });
}

/***/ }),

/***/ 3:
/*!*********************************!*\
  !*** multi ./src/js/reports.js ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! ./src/js/reports.js */"./src/js/reports.js");


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vc3JjL2pzL3JlcG9ydHMuanMiXSwibmFtZXMiOlsid2luZG93IiwibHVtZW4iLCJjb25maXJtRGVsZXRlUmVwb3J0IiwidHJpZ2dlclJlcG9ydFN0YXJ0UGF1c2UiLCJsaW5rIiwicmVwb3J0TmFtZSIsImRhdGFzZXQiLCJhbnN3ZXIiLCJjb25maXJtIiwicG9zdEFzRm9ybSIsImhyZWYiLCJyZXBvcnRfbmFtZSIsImlucHV0IiwidXJsIiwicGF1c2VVcmwiLCJlbmNvZGVVUklDb21wb25lbnQiLCJpc1BhdXNlZCIsImNoZWNrZWQiLCJkYXRhIiwiRm9ybURhdGEiLCJhcHBlbmQiLCJjc3JmVG9rZW4iLCJDU1JGIiwiZmV0Y2giLCJtZXRob2QiLCJib2R5IiwidGhlbiIsInJlc3BvbnNlIiwib2siLCIkIiwib2ZmIl0sIm1hcHBpbmdzIjoiO1FBQUE7UUFDQTs7UUFFQTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBOztRQUVBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7OztRQUdBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7UUFDQSwwQ0FBMEMsZ0NBQWdDO1FBQzFFO1FBQ0E7O1FBRUE7UUFDQTtRQUNBO1FBQ0Esd0RBQXdELGtCQUFrQjtRQUMxRTtRQUNBLGlEQUFpRCxjQUFjO1FBQy9EOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQSx5Q0FBeUMsaUNBQWlDO1FBQzFFLGdIQUFnSCxtQkFBbUIsRUFBRTtRQUNySTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBLDJCQUEyQiwwQkFBMEIsRUFBRTtRQUN2RCxpQ0FBaUMsZUFBZTtRQUNoRDtRQUNBO1FBQ0E7O1FBRUE7UUFDQSxzREFBc0QsK0RBQStEOztRQUVySDtRQUNBOzs7UUFHQTtRQUNBOzs7Ozs7Ozs7Ozs7QUNsRkE7QUFFQTtBQUNBQSxNQUFNLENBQUNDLEtBQVAsR0FBZTtBQUNiQyxxQkFBbUIsRUFBbkJBLG1CQURhO0FBRWJDLHlCQUF1QixFQUF2QkE7QUFGYSxDQUFmO0FBS0E7Ozs7OztBQU1BOztBQUNBLFNBQVNELG1CQUFULENBQTZCRSxJQUE3QixFQUFtQztBQUNqQyxNQUFNQyxVQUFVLEdBQUdELElBQUksQ0FBQ0UsT0FBTCxDQUFhRCxVQUFoQztBQUNBLE1BQU1FLE1BQU0sR0FBR0MsT0FBTyw2Q0FDZ0JILFVBRGhCLGdCQUF0Qjs7QUFHQSxNQUFJRSxNQUFKLEVBQVk7QUFDVkUsY0FBVSxDQUFDTCxJQUFJLENBQUNNLElBQU4sRUFBWTtBQUNwQkMsaUJBQVcsRUFBRU47QUFETyxLQUFaLENBQVY7QUFHRDs7QUFFRCxTQUFPLEtBQVA7QUFDRDtBQUVEOzs7Ozs7O0FBS0EsU0FBU0YsdUJBQVQsQ0FBaUNTLEtBQWpDLEVBQXdDO0FBQ3RDLE1BQUlDLEdBQUcsR0FBR0QsS0FBSyxDQUFDTixPQUFOLENBQWNRLFFBQXhCO0FBQ0EsTUFBTVQsVUFBVSxHQUFHVSxrQkFBa0IsQ0FBQ0gsS0FBSyxDQUFDTixPQUFOLENBQWNELFVBQWYsQ0FBckM7QUFDQSxNQUFNVyxRQUFRLEdBQUdKLEtBQUssQ0FBQ0ssT0FBdkI7QUFFQUosS0FBRyxhQUFNQSxHQUFOLDBCQUF5QlIsVUFBekIsd0JBQWlEVyxRQUFqRCxDQUFIO0FBQ0EsTUFBTUUsSUFBSSxHQUFHLElBQUlDLFFBQUosRUFBYjtBQUNBRCxNQUFJLENBQUNFLE1BQUwsQ0FDRSxZQURGLEVBRUUsT0FBT0MsU0FBUCxLQUFxQixXQUFyQixJQUFvQ0EsU0FBUyxLQUFLLElBQWxELEdBQXlEQyxJQUF6RCxHQUFnRUQsU0FGbEU7QUFLQUUsT0FBSyxDQUFDVixHQUFELEVBQU07QUFDVFcsVUFBTSxFQUFFLE1BREM7QUFFVEMsUUFBSSxFQUFFUDtBQUZHLEdBQU4sQ0FBTCxDQUdHUSxJQUhILENBR1EsVUFBQ0MsUUFBRCxFQUFjO0FBQ3BCLFFBQUksQ0FBQ0EsUUFBUSxDQUFDQyxFQUFkLEVBQWtCO0FBQ2hCQyxPQUFDLENBQUNqQixLQUFELENBQUQsQ0FBU00sSUFBVCxDQUFjLFdBQWQsRUFBMkJZLEdBQTNCLENBQStCLENBQUNkLFFBQWhDO0FBQ0Q7QUFDRixHQVBEO0FBUUQsQyIsImZpbGUiOiJyZXBvcnRzLmpzIiwic291cmNlc0NvbnRlbnQiOlsiIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbiBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblxuIFx0XHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcbiBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbiBcdFx0XHRyZXR1cm4gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0uZXhwb3J0cztcbiBcdFx0fVxuIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuIFx0XHR2YXIgbW9kdWxlID0gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0gPSB7XG4gXHRcdFx0aTogbW9kdWxlSWQsXG4gXHRcdFx0bDogZmFsc2UsXG4gXHRcdFx0ZXhwb3J0czoge31cbiBcdFx0fTtcblxuIFx0XHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cbiBcdFx0bW9kdWxlc1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cbiBcdFx0Ly8gRmxhZyB0aGUgbW9kdWxlIGFzIGxvYWRlZFxuIFx0XHRtb2R1bGUubCA9IHRydWU7XG5cbiBcdFx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcbiBcdFx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xuIFx0fVxuXG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm0gPSBtb2R1bGVzO1xuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5jID0gaW5zdGFsbGVkTW9kdWxlcztcblxuIFx0Ly8gZGVmaW5lIGdldHRlciBmdW5jdGlvbiBmb3IgaGFybW9ueSBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQgPSBmdW5jdGlvbihleHBvcnRzLCBuYW1lLCBnZXR0ZXIpIHtcbiBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBuYW1lLCB7IGVudW1lcmFibGU6IHRydWUsIGdldDogZ2V0dGVyIH0pO1xuIFx0XHR9XG4gXHR9O1xuXG4gXHQvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSBmdW5jdGlvbihleHBvcnRzKSB7XG4gXHRcdGlmKHR5cGVvZiBTeW1ib2wgIT09ICd1bmRlZmluZWQnICYmIFN5bWJvbC50b1N0cmluZ1RhZykge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBTeW1ib2wudG9TdHJpbmdUYWcsIHsgdmFsdWU6ICdNb2R1bGUnIH0pO1xuIFx0XHR9XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCAnX19lc01vZHVsZScsIHsgdmFsdWU6IHRydWUgfSk7XG4gXHR9O1xuXG4gXHQvLyBjcmVhdGUgYSBmYWtlIG5hbWVzcGFjZSBvYmplY3RcbiBcdC8vIG1vZGUgJiAxOiB2YWx1ZSBpcyBhIG1vZHVsZSBpZCwgcmVxdWlyZSBpdFxuIFx0Ly8gbW9kZSAmIDI6IG1lcmdlIGFsbCBwcm9wZXJ0aWVzIG9mIHZhbHVlIGludG8gdGhlIG5zXG4gXHQvLyBtb2RlICYgNDogcmV0dXJuIHZhbHVlIHdoZW4gYWxyZWFkeSBucyBvYmplY3RcbiBcdC8vIG1vZGUgJiA4fDE6IGJlaGF2ZSBsaWtlIHJlcXVpcmVcbiBcdF9fd2VicGFja19yZXF1aXJlX18udCA9IGZ1bmN0aW9uKHZhbHVlLCBtb2RlKSB7XG4gXHRcdGlmKG1vZGUgJiAxKSB2YWx1ZSA9IF9fd2VicGFja19yZXF1aXJlX18odmFsdWUpO1xuIFx0XHRpZihtb2RlICYgOCkgcmV0dXJuIHZhbHVlO1xuIFx0XHRpZigobW9kZSAmIDQpICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcgJiYgdmFsdWUgJiYgdmFsdWUuX19lc01vZHVsZSkgcmV0dXJuIHZhbHVlO1xuIFx0XHR2YXIgbnMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIobnMpO1xuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkobnMsICdkZWZhdWx0JywgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdmFsdWUgfSk7XG4gXHRcdGlmKG1vZGUgJiAyICYmIHR5cGVvZiB2YWx1ZSAhPSAnc3RyaW5nJykgZm9yKHZhciBrZXkgaW4gdmFsdWUpIF9fd2VicGFja19yZXF1aXJlX18uZChucywga2V5LCBmdW5jdGlvbihrZXkpIHsgcmV0dXJuIHZhbHVlW2tleV07IH0uYmluZChudWxsLCBrZXkpKTtcbiBcdFx0cmV0dXJuIG5zO1xuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcblxuXG4gXHQvLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbiBcdHJldHVybiBfX3dlYnBhY2tfcmVxdWlyZV9fKF9fd2VicGFja19yZXF1aXJlX18ucyA9IDMpO1xuIiwiLypnbG9iYWwgcG9zdEFzRm9ybSAqL1xuXG4vLyBleHBvc2UgbHVtZW4gQVBJXG53aW5kb3cubHVtZW4gPSB7XG4gIGNvbmZpcm1EZWxldGVSZXBvcnQsXG4gIHRyaWdnZXJSZXBvcnRTdGFydFBhdXNlLFxufTtcblxuLyoqXG4gKiBEZWxldGUgcmVwb3J0LlxuICogQXNrIHVzZXIgZm9yIGNvbmZpcm1hdGlvbiBwcmlvciB0byBzZW5kaW5nIGEgcmVxdWVzdC5cbiAqXG4gKiBAcGFyYW0ge0hUTUxFbGVtZW50fSBsaW5rIGh0bWwgZWxlbWVudCB0aGUgZnVuY3Rpb24gaXMgY2FsbGVkIG9uXG4gKi9cbi8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby11bnVzZWQtdmFyc1xuZnVuY3Rpb24gY29uZmlybURlbGV0ZVJlcG9ydChsaW5rKSB7XG4gIGNvbnN0IHJlcG9ydE5hbWUgPSBsaW5rLmRhdGFzZXQucmVwb3J0TmFtZTtcbiAgY29uc3QgYW5zd2VyID0gY29uZmlybShcbiAgICBgQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIGRlbGV0ZSBcIiR7cmVwb3J0TmFtZX1cIiByZXBvcnQ/YFxuICApO1xuICBpZiAoYW5zd2VyKSB7XG4gICAgcG9zdEFzRm9ybShsaW5rLmhyZWYsIHtcbiAgICAgIHJlcG9ydF9uYW1lOiByZXBvcnROYW1lLFxuICAgIH0pO1xuICB9XG5cbiAgcmV0dXJuIGZhbHNlO1xufVxuXG4vKipcbiAqIFN0YXJ0L1BhdXNlIHJlcG9ydCB0cmlnZ2VyIGhhbmRsZXIuXG4gKlxuICogQHBhcmFtIHtIVE1MRWxlbWVudH0gaW5wdXQgaHRtbCBpbnB1dCBlbGVtZW50IHRoZSBmdW5jdGlvbiBpcyBjYWxsZWQgb25cbiAqL1xuZnVuY3Rpb24gdHJpZ2dlclJlcG9ydFN0YXJ0UGF1c2UoaW5wdXQpIHtcbiAgbGV0IHVybCA9IGlucHV0LmRhdGFzZXQucGF1c2VVcmw7XG4gIGNvbnN0IHJlcG9ydE5hbWUgPSBlbmNvZGVVUklDb21wb25lbnQoaW5wdXQuZGF0YXNldC5yZXBvcnROYW1lKTtcbiAgY29uc3QgaXNQYXVzZWQgPSBpbnB1dC5jaGVja2VkO1xuXG4gIHVybCA9IGAke3VybH0/cmVwb3J0X25hbWU9JHtyZXBvcnROYW1lfSZpc19wYXVzZWQ9JHtpc1BhdXNlZH1gO1xuICBjb25zdCBkYXRhID0gbmV3IEZvcm1EYXRhKCk7XG4gIGRhdGEuYXBwZW5kKFxuICAgIFwiY3NyZl90b2tlblwiLFxuICAgIHR5cGVvZiBjc3JmVG9rZW4gPT09IFwidW5kZWZpbmVkXCIgfHwgY3NyZlRva2VuID09PSBudWxsID8gQ1NSRiA6IGNzcmZUb2tlblxuICApO1xuXG4gIGZldGNoKHVybCwge1xuICAgIG1ldGhvZDogXCJQT1NUXCIsXG4gICAgYm9keTogZGF0YSxcbiAgfSkudGhlbigocmVzcG9uc2UpID0+IHtcbiAgICBpZiAoIXJlc3BvbnNlLm9rKSB7XG4gICAgICAkKGlucHV0KS5kYXRhKFwiYnMudG9nZ2xlXCIpLm9mZighaXNQYXVzZWQpO1xuICAgIH1cbiAgfSk7XG59XG4iXSwic291cmNlUm9vdCI6IiJ9