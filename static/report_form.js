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

/* global isRBAC, moment */
(function reportFormSetUp() {
  var scheduleTypeInput = document.getElementById("schedule_type");
  var scheduleWeekDayInput = document.getElementById("schedule_week_day");
  var scheduleWeekDayRow = scheduleWeekDayInput.closest("tr") || scheduleWeekDayInput.closest(".form-group");
  var scheduleTimeInput = document.getElementById("schedule_time");
  var scheduleTimeRow = scheduleTimeInput.closest("tr") || scheduleTimeInput.closest(".form-group");
  var scheduleCustomInput = document.getElementById("schedule_custom");
  var scheduleCustomRow = scheduleCustomInput.closest("tr") || scheduleCustomInput.closest(".form-group");
  var scheduleTimezoneInput = document.getElementById("schedule_timezone"); // read time and weekDay while it's in UTC

  var time = scheduleTimeInput.value;
  var weekDay = scheduleWeekDayInput.value;
  var timeZone = getClientTimezone(); // detect currently selected schedule type and
  // display appropriate fields

  configureScheduleUI(scheduleTypeInput.value);
  $(scheduleTypeInput).on("change", function ($event) {
    configureScheduleUI($event.target.value);
  });
  /**
   * Configure schedule UI according to the schedule type
   *
   * @param {string} scheduleType type of the schedule
   */

  function configureScheduleUI(scheduleType) {
    scheduleTimezoneInput.value = timeZone;

    switch (scheduleType) {
      case "daily":
        if (isRBAC === true) {
          convertToClientTimezone();
        }

        enableDailySchedule();
        break;

      case "weekly":
        if (isRBAC === true) {
          convertToClientTimezone();
        }

        enableWeeklySchedule();
        break;

      case "custom":
        enableCustomSchedule();
        break;

      default:
        enableManualSchedule();
        break;
    }
  }
  /**
   * Retrieve airflow client timezone
   */


  function getClientTimezone() {
    return localStorage.getItem("selected-timezone") || localStorage.getItem("chosen-timezone");
  }
  /**
   * Convert schedule from UTC to client timezone
   */


  function convertToClientTimezone() {
    if (!time) {
      return;
    }

    var dateTimeUTC = moment.utc(time, "HH:mm");

    if (weekDay) {
      dateTimeUTC.day(Number(weekDay));
    }

    var dateTimeInClientTZ = dateTimeUTC.clone().tz(timeZone);
    scheduleTimeInput.value = dateTimeInClientTZ.format("HH:mm");
    scheduleWeekDayInput.value = String(dateTimeInClientTZ.day());
  }
  /**
   * Display daily schedule fields
   */


  function enableDailySchedule() {
    scheduleTimeRow.hidden = false;
    scheduleWeekDayRow.hidden = true;
    scheduleCustomRow.hidden = true;
    scheduleTimeInput.required = true;
    scheduleWeekDayInput.required = false;
    scheduleCustomInput.required = false;
  }
  /**
   * Display weekly schedule fields
   */


  function enableWeeklySchedule() {
    scheduleTimeRow.hidden = false;
    scheduleWeekDayRow.hidden = false;
    scheduleCustomRow.hidden = true;
    scheduleTimeInput.required = true;
    scheduleWeekDayInput.required = true;
    scheduleCustomInput.required = false;
  }
  /**
   * Display custom schedule fields
   */


  function enableCustomSchedule() {
    scheduleTimeRow.hidden = true;
    scheduleWeekDayRow.hidden = true;
    scheduleCustomRow.hidden = false;
    scheduleTimeInput.required = false;
    scheduleWeekDayInput.required = false;
    scheduleCustomInput.required = true;
  }
  /**
   * Hide all schedule fields (manual triggering option)
   */


  function enableManualSchedule() {
    scheduleTimeRow.hidden = true;
    scheduleWeekDayRow.hidden = true;
    scheduleCustomRow.hidden = true;
    scheduleTimeInput.required = false;
    scheduleWeekDayInput.required = false;
    scheduleCustomInput.required = false;
  }
})();

/***/ }),

/***/ 2:
/*!*************************************!*\
  !*** multi ./src/js/report_form.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! ./src/js/report_form.js */"./src/js/report_form.js");


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vc3JjL2pzL3JlcG9ydF9mb3JtLmpzIl0sIm5hbWVzIjpbInJlcG9ydEZvcm1TZXRVcCIsInNjaGVkdWxlVHlwZUlucHV0IiwiZG9jdW1lbnQiLCJnZXRFbGVtZW50QnlJZCIsInNjaGVkdWxlV2Vla0RheUlucHV0Iiwic2NoZWR1bGVXZWVrRGF5Um93IiwiY2xvc2VzdCIsInNjaGVkdWxlVGltZUlucHV0Iiwic2NoZWR1bGVUaW1lUm93Iiwic2NoZWR1bGVDdXN0b21JbnB1dCIsInNjaGVkdWxlQ3VzdG9tUm93Iiwic2NoZWR1bGVUaW1lem9uZUlucHV0IiwidGltZSIsInZhbHVlIiwid2Vla0RheSIsInRpbWVab25lIiwiZ2V0Q2xpZW50VGltZXpvbmUiLCJjb25maWd1cmVTY2hlZHVsZVVJIiwiJCIsIm9uIiwiJGV2ZW50IiwidGFyZ2V0Iiwic2NoZWR1bGVUeXBlIiwiaXNSQkFDIiwiY29udmVydFRvQ2xpZW50VGltZXpvbmUiLCJlbmFibGVEYWlseVNjaGVkdWxlIiwiZW5hYmxlV2Vla2x5U2NoZWR1bGUiLCJlbmFibGVDdXN0b21TY2hlZHVsZSIsImVuYWJsZU1hbnVhbFNjaGVkdWxlIiwibG9jYWxTdG9yYWdlIiwiZ2V0SXRlbSIsImRhdGVUaW1lVVRDIiwibW9tZW50IiwidXRjIiwiZGF5IiwiTnVtYmVyIiwiZGF0ZVRpbWVJbkNsaWVudFRaIiwiY2xvbmUiLCJ0eiIsImZvcm1hdCIsIlN0cmluZyIsImhpZGRlbiIsInJlcXVpcmVkIl0sIm1hcHBpbmdzIjoiO1FBQUE7UUFDQTs7UUFFQTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBOztRQUVBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7OztRQUdBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7UUFDQSwwQ0FBMEMsZ0NBQWdDO1FBQzFFO1FBQ0E7O1FBRUE7UUFDQTtRQUNBO1FBQ0Esd0RBQXdELGtCQUFrQjtRQUMxRTtRQUNBLGlEQUFpRCxjQUFjO1FBQy9EOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQSx5Q0FBeUMsaUNBQWlDO1FBQzFFLGdIQUFnSCxtQkFBbUIsRUFBRTtRQUNySTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBLDJCQUEyQiwwQkFBMEIsRUFBRTtRQUN2RCxpQ0FBaUMsZUFBZTtRQUNoRDtRQUNBO1FBQ0E7O1FBRUE7UUFDQSxzREFBc0QsK0RBQStEOztRQUVySDtRQUNBOzs7UUFHQTtRQUNBOzs7Ozs7Ozs7Ozs7QUNsRkE7QUFFQSxDQUFDLFNBQVNBLGVBQVQsR0FBMkI7QUFDMUIsTUFBTUMsaUJBQWlCLEdBQUdDLFFBQVEsQ0FBQ0MsY0FBVCxDQUF3QixlQUF4QixDQUExQjtBQUNBLE1BQU1DLG9CQUFvQixHQUFHRixRQUFRLENBQUNDLGNBQVQsQ0FBd0IsbUJBQXhCLENBQTdCO0FBQ0EsTUFBTUUsa0JBQWtCLEdBQ3RCRCxvQkFBb0IsQ0FBQ0UsT0FBckIsQ0FBNkIsSUFBN0IsS0FDQUYsb0JBQW9CLENBQUNFLE9BQXJCLENBQTZCLGFBQTdCLENBRkY7QUFHQSxNQUFNQyxpQkFBaUIsR0FBR0wsUUFBUSxDQUFDQyxjQUFULENBQXdCLGVBQXhCLENBQTFCO0FBQ0EsTUFBTUssZUFBZSxHQUNuQkQsaUJBQWlCLENBQUNELE9BQWxCLENBQTBCLElBQTFCLEtBQW1DQyxpQkFBaUIsQ0FBQ0QsT0FBbEIsQ0FBMEIsYUFBMUIsQ0FEckM7QUFFQSxNQUFNRyxtQkFBbUIsR0FBR1AsUUFBUSxDQUFDQyxjQUFULENBQXdCLGlCQUF4QixDQUE1QjtBQUNBLE1BQU1PLGlCQUFpQixHQUNyQkQsbUJBQW1CLENBQUNILE9BQXBCLENBQTRCLElBQTVCLEtBQ0FHLG1CQUFtQixDQUFDSCxPQUFwQixDQUE0QixhQUE1QixDQUZGO0FBR0EsTUFBTUsscUJBQXFCLEdBQUdULFFBQVEsQ0FBQ0MsY0FBVCxDQUF3QixtQkFBeEIsQ0FBOUIsQ0FiMEIsQ0FlMUI7O0FBQ0EsTUFBTVMsSUFBSSxHQUFHTCxpQkFBaUIsQ0FBQ00sS0FBL0I7QUFDQSxNQUFNQyxPQUFPLEdBQUdWLG9CQUFvQixDQUFDUyxLQUFyQztBQUNBLE1BQU1FLFFBQVEsR0FBR0MsaUJBQWlCLEVBQWxDLENBbEIwQixDQW9CMUI7QUFDQTs7QUFDQUMscUJBQW1CLENBQUNoQixpQkFBaUIsQ0FBQ1ksS0FBbkIsQ0FBbkI7QUFFQUssR0FBQyxDQUFDakIsaUJBQUQsQ0FBRCxDQUFxQmtCLEVBQXJCLENBQXdCLFFBQXhCLEVBQWtDLFVBQUNDLE1BQUQsRUFBWTtBQUM1Q0gsdUJBQW1CLENBQUNHLE1BQU0sQ0FBQ0MsTUFBUCxDQUFjUixLQUFmLENBQW5CO0FBQ0QsR0FGRDtBQUlBOzs7Ozs7QUFLQSxXQUFTSSxtQkFBVCxDQUE2QkssWUFBN0IsRUFBMkM7QUFDekNYLHlCQUFxQixDQUFDRSxLQUF0QixHQUE4QkUsUUFBOUI7O0FBRUEsWUFBUU8sWUFBUjtBQUNFLFdBQUssT0FBTDtBQUNFLFlBQUlDLE1BQU0sS0FBSyxJQUFmLEVBQXFCO0FBQ25CQyxpQ0FBdUI7QUFDeEI7O0FBQ0RDLDJCQUFtQjtBQUNuQjs7QUFDRixXQUFLLFFBQUw7QUFDRSxZQUFJRixNQUFNLEtBQUssSUFBZixFQUFxQjtBQUNuQkMsaUNBQXVCO0FBQ3hCOztBQUNERSw0QkFBb0I7QUFDcEI7O0FBQ0YsV0FBSyxRQUFMO0FBQ0VDLDRCQUFvQjtBQUNwQjs7QUFDRjtBQUNFQyw0QkFBb0I7QUFDcEI7QUFsQko7QUFvQkQ7QUFFRDs7Ozs7QUFHQSxXQUFTWixpQkFBVCxHQUE2QjtBQUMzQixXQUNFYSxZQUFZLENBQUNDLE9BQWIsQ0FBcUIsbUJBQXJCLEtBQ0FELFlBQVksQ0FBQ0MsT0FBYixDQUFxQixpQkFBckIsQ0FGRjtBQUlEO0FBRUQ7Ozs7O0FBR0EsV0FBU04sdUJBQVQsR0FBbUM7QUFDakMsUUFBSSxDQUFDWixJQUFMLEVBQVc7QUFDVDtBQUNEOztBQUVELFFBQU1tQixXQUFXLEdBQUdDLE1BQU0sQ0FBQ0MsR0FBUCxDQUFXckIsSUFBWCxFQUFpQixPQUFqQixDQUFwQjs7QUFDQSxRQUFJRSxPQUFKLEVBQWE7QUFDWGlCLGlCQUFXLENBQUNHLEdBQVosQ0FBZ0JDLE1BQU0sQ0FBQ3JCLE9BQUQsQ0FBdEI7QUFDRDs7QUFFRCxRQUFNc0Isa0JBQWtCLEdBQUdMLFdBQVcsQ0FBQ00sS0FBWixHQUFvQkMsRUFBcEIsQ0FBdUJ2QixRQUF2QixDQUEzQjtBQUNBUixxQkFBaUIsQ0FBQ00sS0FBbEIsR0FBMEJ1QixrQkFBa0IsQ0FBQ0csTUFBbkIsQ0FBMEIsT0FBMUIsQ0FBMUI7QUFDQW5DLHdCQUFvQixDQUFDUyxLQUFyQixHQUE2QjJCLE1BQU0sQ0FBQ0osa0JBQWtCLENBQUNGLEdBQW5CLEVBQUQsQ0FBbkM7QUFDRDtBQUVEOzs7OztBQUdBLFdBQVNULG1CQUFULEdBQStCO0FBQzdCakIsbUJBQWUsQ0FBQ2lDLE1BQWhCLEdBQXlCLEtBQXpCO0FBQ0FwQyxzQkFBa0IsQ0FBQ29DLE1BQW5CLEdBQTRCLElBQTVCO0FBQ0EvQixxQkFBaUIsQ0FBQytCLE1BQWxCLEdBQTJCLElBQTNCO0FBRUFsQyxxQkFBaUIsQ0FBQ21DLFFBQWxCLEdBQTZCLElBQTdCO0FBQ0F0Qyx3QkFBb0IsQ0FBQ3NDLFFBQXJCLEdBQWdDLEtBQWhDO0FBQ0FqQyx1QkFBbUIsQ0FBQ2lDLFFBQXBCLEdBQStCLEtBQS9CO0FBQ0Q7QUFFRDs7Ozs7QUFHQSxXQUFTaEIsb0JBQVQsR0FBZ0M7QUFDOUJsQixtQkFBZSxDQUFDaUMsTUFBaEIsR0FBeUIsS0FBekI7QUFDQXBDLHNCQUFrQixDQUFDb0MsTUFBbkIsR0FBNEIsS0FBNUI7QUFDQS9CLHFCQUFpQixDQUFDK0IsTUFBbEIsR0FBMkIsSUFBM0I7QUFFQWxDLHFCQUFpQixDQUFDbUMsUUFBbEIsR0FBNkIsSUFBN0I7QUFDQXRDLHdCQUFvQixDQUFDc0MsUUFBckIsR0FBZ0MsSUFBaEM7QUFDQWpDLHVCQUFtQixDQUFDaUMsUUFBcEIsR0FBK0IsS0FBL0I7QUFDRDtBQUVEOzs7OztBQUdBLFdBQVNmLG9CQUFULEdBQWdDO0FBQzlCbkIsbUJBQWUsQ0FBQ2lDLE1BQWhCLEdBQXlCLElBQXpCO0FBQ0FwQyxzQkFBa0IsQ0FBQ29DLE1BQW5CLEdBQTRCLElBQTVCO0FBQ0EvQixxQkFBaUIsQ0FBQytCLE1BQWxCLEdBQTJCLEtBQTNCO0FBRUFsQyxxQkFBaUIsQ0FBQ21DLFFBQWxCLEdBQTZCLEtBQTdCO0FBQ0F0Qyx3QkFBb0IsQ0FBQ3NDLFFBQXJCLEdBQWdDLEtBQWhDO0FBQ0FqQyx1QkFBbUIsQ0FBQ2lDLFFBQXBCLEdBQStCLElBQS9CO0FBQ0Q7QUFFRDs7Ozs7QUFHQSxXQUFTZCxvQkFBVCxHQUFnQztBQUM5QnBCLG1CQUFlLENBQUNpQyxNQUFoQixHQUF5QixJQUF6QjtBQUNBcEMsc0JBQWtCLENBQUNvQyxNQUFuQixHQUE0QixJQUE1QjtBQUNBL0IscUJBQWlCLENBQUMrQixNQUFsQixHQUEyQixJQUEzQjtBQUVBbEMscUJBQWlCLENBQUNtQyxRQUFsQixHQUE2QixLQUE3QjtBQUNBdEMsd0JBQW9CLENBQUNzQyxRQUFyQixHQUFnQyxLQUFoQztBQUNBakMsdUJBQW1CLENBQUNpQyxRQUFwQixHQUErQixLQUEvQjtBQUNEO0FBQ0YsQ0F6SUQsSSIsImZpbGUiOiJyZXBvcnRfZm9ybS5qcyIsInNvdXJjZXNDb250ZW50IjpbIiBcdC8vIFRoZSBtb2R1bGUgY2FjaGVcbiBcdHZhciBpbnN0YWxsZWRNb2R1bGVzID0ge307XG5cbiBcdC8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG4gXHRmdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cbiBcdFx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG4gXHRcdGlmKGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdKSB7XG4gXHRcdFx0cmV0dXJuIGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdLmV4cG9ydHM7XG4gXHRcdH1cbiBcdFx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcbiBcdFx0dmFyIG1vZHVsZSA9IGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdID0ge1xuIFx0XHRcdGk6IG1vZHVsZUlkLFxuIFx0XHRcdGw6IGZhbHNlLFxuIFx0XHRcdGV4cG9ydHM6IHt9XG4gXHRcdH07XG5cbiBcdFx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG4gXHRcdG1vZHVsZXNbbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG4gXHRcdC8vIEZsYWcgdGhlIG1vZHVsZSBhcyBsb2FkZWRcbiBcdFx0bW9kdWxlLmwgPSB0cnVlO1xuXG4gXHRcdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG4gXHRcdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbiBcdH1cblxuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZXMgb2JqZWN0IChfX3dlYnBhY2tfbW9kdWxlc19fKVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5tID0gbW9kdWxlcztcblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGUgY2FjaGVcbiBcdF9fd2VicGFja19yZXF1aXJlX18uYyA9IGluc3RhbGxlZE1vZHVsZXM7XG5cbiBcdC8vIGRlZmluZSBnZXR0ZXIgZnVuY3Rpb24gZm9yIGhhcm1vbnkgZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kID0gZnVuY3Rpb24oZXhwb3J0cywgbmFtZSwgZ2V0dGVyKSB7XG4gXHRcdGlmKCFfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZXhwb3J0cywgbmFtZSkpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgbmFtZSwgeyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGdldHRlciB9KTtcbiBcdFx0fVxuIFx0fTtcblxuIFx0Ly8gZGVmaW5lIF9fZXNNb2R1bGUgb24gZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yID0gZnVuY3Rpb24oZXhwb3J0cykge1xuIFx0XHRpZih0eXBlb2YgU3ltYm9sICE9PSAndW5kZWZpbmVkJyAmJiBTeW1ib2wudG9TdHJpbmdUYWcpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgU3ltYm9sLnRvU3RyaW5nVGFnLCB7IHZhbHVlOiAnTW9kdWxlJyB9KTtcbiBcdFx0fVxuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgJ19fZXNNb2R1bGUnLCB7IHZhbHVlOiB0cnVlIH0pO1xuIFx0fTtcblxuIFx0Ly8gY3JlYXRlIGEgZmFrZSBuYW1lc3BhY2Ugb2JqZWN0XG4gXHQvLyBtb2RlICYgMTogdmFsdWUgaXMgYSBtb2R1bGUgaWQsIHJlcXVpcmUgaXRcbiBcdC8vIG1vZGUgJiAyOiBtZXJnZSBhbGwgcHJvcGVydGllcyBvZiB2YWx1ZSBpbnRvIHRoZSBuc1xuIFx0Ly8gbW9kZSAmIDQ6IHJldHVybiB2YWx1ZSB3aGVuIGFscmVhZHkgbnMgb2JqZWN0XG4gXHQvLyBtb2RlICYgOHwxOiBiZWhhdmUgbGlrZSByZXF1aXJlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnQgPSBmdW5jdGlvbih2YWx1ZSwgbW9kZSkge1xuIFx0XHRpZihtb2RlICYgMSkgdmFsdWUgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKHZhbHVlKTtcbiBcdFx0aWYobW9kZSAmIDgpIHJldHVybiB2YWx1ZTtcbiBcdFx0aWYoKG1vZGUgJiA0KSAmJiB0eXBlb2YgdmFsdWUgPT09ICdvYmplY3QnICYmIHZhbHVlICYmIHZhbHVlLl9fZXNNb2R1bGUpIHJldHVybiB2YWx1ZTtcbiBcdFx0dmFyIG5zID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yKG5zKTtcbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KG5zLCAnZGVmYXVsdCcsIHsgZW51bWVyYWJsZTogdHJ1ZSwgdmFsdWU6IHZhbHVlIH0pO1xuIFx0XHRpZihtb2RlICYgMiAmJiB0eXBlb2YgdmFsdWUgIT0gJ3N0cmluZycpIGZvcih2YXIga2V5IGluIHZhbHVlKSBfX3dlYnBhY2tfcmVxdWlyZV9fLmQobnMsIGtleSwgZnVuY3Rpb24oa2V5KSB7IHJldHVybiB2YWx1ZVtrZXldOyB9LmJpbmQobnVsbCwga2V5KSk7XG4gXHRcdHJldHVybiBucztcbiBcdH07XG5cbiBcdC8vIGdldERlZmF1bHRFeHBvcnQgZnVuY3Rpb24gZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBub24taGFybW9ueSBtb2R1bGVzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm4gPSBmdW5jdGlvbihtb2R1bGUpIHtcbiBcdFx0dmFyIGdldHRlciA9IG1vZHVsZSAmJiBtb2R1bGUuX19lc01vZHVsZSA/XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0RGVmYXVsdCgpIHsgcmV0dXJuIG1vZHVsZVsnZGVmYXVsdCddOyB9IDpcbiBcdFx0XHRmdW5jdGlvbiBnZXRNb2R1bGVFeHBvcnRzKCkgeyByZXR1cm4gbW9kdWxlOyB9O1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQoZ2V0dGVyLCAnYScsIGdldHRlcik7XG4gXHRcdHJldHVybiBnZXR0ZXI7XG4gXHR9O1xuXG4gXHQvLyBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGxcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubyA9IGZ1bmN0aW9uKG9iamVjdCwgcHJvcGVydHkpIHsgcmV0dXJuIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmplY3QsIHByb3BlcnR5KTsgfTtcblxuIFx0Ly8gX193ZWJwYWNrX3B1YmxpY19wYXRoX19cbiBcdF9fd2VicGFja19yZXF1aXJlX18ucCA9IFwiXCI7XG5cblxuIFx0Ly8gTG9hZCBlbnRyeSBtb2R1bGUgYW5kIHJldHVybiBleHBvcnRzXG4gXHRyZXR1cm4gX193ZWJwYWNrX3JlcXVpcmVfXyhfX3dlYnBhY2tfcmVxdWlyZV9fLnMgPSAyKTtcbiIsIi8qIGdsb2JhbCBpc1JCQUMsIG1vbWVudCAqL1xuXG4oZnVuY3Rpb24gcmVwb3J0Rm9ybVNldFVwKCkge1xuICBjb25zdCBzY2hlZHVsZVR5cGVJbnB1dCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKFwic2NoZWR1bGVfdHlwZVwiKTtcbiAgY29uc3Qgc2NoZWR1bGVXZWVrRGF5SW5wdXQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChcInNjaGVkdWxlX3dlZWtfZGF5XCIpO1xuICBjb25zdCBzY2hlZHVsZVdlZWtEYXlSb3cgPVxuICAgIHNjaGVkdWxlV2Vla0RheUlucHV0LmNsb3Nlc3QoXCJ0clwiKSB8fFxuICAgIHNjaGVkdWxlV2Vla0RheUlucHV0LmNsb3Nlc3QoXCIuZm9ybS1ncm91cFwiKTtcbiAgY29uc3Qgc2NoZWR1bGVUaW1lSW5wdXQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChcInNjaGVkdWxlX3RpbWVcIik7XG4gIGNvbnN0IHNjaGVkdWxlVGltZVJvdyA9XG4gICAgc2NoZWR1bGVUaW1lSW5wdXQuY2xvc2VzdChcInRyXCIpIHx8IHNjaGVkdWxlVGltZUlucHV0LmNsb3Nlc3QoXCIuZm9ybS1ncm91cFwiKTtcbiAgY29uc3Qgc2NoZWR1bGVDdXN0b21JbnB1dCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKFwic2NoZWR1bGVfY3VzdG9tXCIpO1xuICBjb25zdCBzY2hlZHVsZUN1c3RvbVJvdyA9XG4gICAgc2NoZWR1bGVDdXN0b21JbnB1dC5jbG9zZXN0KFwidHJcIikgfHxcbiAgICBzY2hlZHVsZUN1c3RvbUlucHV0LmNsb3Nlc3QoXCIuZm9ybS1ncm91cFwiKTtcbiAgY29uc3Qgc2NoZWR1bGVUaW1lem9uZUlucHV0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoXCJzY2hlZHVsZV90aW1lem9uZVwiKTtcblxuICAvLyByZWFkIHRpbWUgYW5kIHdlZWtEYXkgd2hpbGUgaXQncyBpbiBVVENcbiAgY29uc3QgdGltZSA9IHNjaGVkdWxlVGltZUlucHV0LnZhbHVlO1xuICBjb25zdCB3ZWVrRGF5ID0gc2NoZWR1bGVXZWVrRGF5SW5wdXQudmFsdWU7XG4gIGNvbnN0IHRpbWVab25lID0gZ2V0Q2xpZW50VGltZXpvbmUoKTtcblxuICAvLyBkZXRlY3QgY3VycmVudGx5IHNlbGVjdGVkIHNjaGVkdWxlIHR5cGUgYW5kXG4gIC8vIGRpc3BsYXkgYXBwcm9wcmlhdGUgZmllbGRzXG4gIGNvbmZpZ3VyZVNjaGVkdWxlVUkoc2NoZWR1bGVUeXBlSW5wdXQudmFsdWUpO1xuXG4gICQoc2NoZWR1bGVUeXBlSW5wdXQpLm9uKFwiY2hhbmdlXCIsICgkZXZlbnQpID0+IHtcbiAgICBjb25maWd1cmVTY2hlZHVsZVVJKCRldmVudC50YXJnZXQudmFsdWUpO1xuICB9KTtcblxuICAvKipcbiAgICogQ29uZmlndXJlIHNjaGVkdWxlIFVJIGFjY29yZGluZyB0byB0aGUgc2NoZWR1bGUgdHlwZVxuICAgKlxuICAgKiBAcGFyYW0ge3N0cmluZ30gc2NoZWR1bGVUeXBlIHR5cGUgb2YgdGhlIHNjaGVkdWxlXG4gICAqL1xuICBmdW5jdGlvbiBjb25maWd1cmVTY2hlZHVsZVVJKHNjaGVkdWxlVHlwZSkge1xuICAgIHNjaGVkdWxlVGltZXpvbmVJbnB1dC52YWx1ZSA9IHRpbWVab25lO1xuXG4gICAgc3dpdGNoIChzY2hlZHVsZVR5cGUpIHtcbiAgICAgIGNhc2UgXCJkYWlseVwiOlxuICAgICAgICBpZiAoaXNSQkFDID09PSB0cnVlKSB7XG4gICAgICAgICAgY29udmVydFRvQ2xpZW50VGltZXpvbmUoKTtcbiAgICAgICAgfVxuICAgICAgICBlbmFibGVEYWlseVNjaGVkdWxlKCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSBcIndlZWtseVwiOlxuICAgICAgICBpZiAoaXNSQkFDID09PSB0cnVlKSB7XG4gICAgICAgICAgY29udmVydFRvQ2xpZW50VGltZXpvbmUoKTtcbiAgICAgICAgfVxuICAgICAgICBlbmFibGVXZWVrbHlTY2hlZHVsZSgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgXCJjdXN0b21cIjpcbiAgICAgICAgZW5hYmxlQ3VzdG9tU2NoZWR1bGUoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBlbmFibGVNYW51YWxTY2hlZHVsZSgpO1xuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogUmV0cmlldmUgYWlyZmxvdyBjbGllbnQgdGltZXpvbmVcbiAgICovXG4gIGZ1bmN0aW9uIGdldENsaWVudFRpbWV6b25lKCkge1xuICAgIHJldHVybiAoXG4gICAgICBsb2NhbFN0b3JhZ2UuZ2V0SXRlbShcInNlbGVjdGVkLXRpbWV6b25lXCIpIHx8XG4gICAgICBsb2NhbFN0b3JhZ2UuZ2V0SXRlbShcImNob3Nlbi10aW1lem9uZVwiKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQ29udmVydCBzY2hlZHVsZSBmcm9tIFVUQyB0byBjbGllbnQgdGltZXpvbmVcbiAgICovXG4gIGZ1bmN0aW9uIGNvbnZlcnRUb0NsaWVudFRpbWV6b25lKCkge1xuICAgIGlmICghdGltZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IGRhdGVUaW1lVVRDID0gbW9tZW50LnV0Yyh0aW1lLCBcIkhIOm1tXCIpO1xuICAgIGlmICh3ZWVrRGF5KSB7XG4gICAgICBkYXRlVGltZVVUQy5kYXkoTnVtYmVyKHdlZWtEYXkpKTtcbiAgICB9XG5cbiAgICBjb25zdCBkYXRlVGltZUluQ2xpZW50VFogPSBkYXRlVGltZVVUQy5jbG9uZSgpLnR6KHRpbWVab25lKTtcbiAgICBzY2hlZHVsZVRpbWVJbnB1dC52YWx1ZSA9IGRhdGVUaW1lSW5DbGllbnRUWi5mb3JtYXQoXCJISDptbVwiKTtcbiAgICBzY2hlZHVsZVdlZWtEYXlJbnB1dC52YWx1ZSA9IFN0cmluZyhkYXRlVGltZUluQ2xpZW50VFouZGF5KCkpO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3BsYXkgZGFpbHkgc2NoZWR1bGUgZmllbGRzXG4gICAqL1xuICBmdW5jdGlvbiBlbmFibGVEYWlseVNjaGVkdWxlKCkge1xuICAgIHNjaGVkdWxlVGltZVJvdy5oaWRkZW4gPSBmYWxzZTtcbiAgICBzY2hlZHVsZVdlZWtEYXlSb3cuaGlkZGVuID0gdHJ1ZTtcbiAgICBzY2hlZHVsZUN1c3RvbVJvdy5oaWRkZW4gPSB0cnVlO1xuXG4gICAgc2NoZWR1bGVUaW1lSW5wdXQucmVxdWlyZWQgPSB0cnVlO1xuICAgIHNjaGVkdWxlV2Vla0RheUlucHV0LnJlcXVpcmVkID0gZmFsc2U7XG4gICAgc2NoZWR1bGVDdXN0b21JbnB1dC5yZXF1aXJlZCA9IGZhbHNlO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3BsYXkgd2Vla2x5IHNjaGVkdWxlIGZpZWxkc1xuICAgKi9cbiAgZnVuY3Rpb24gZW5hYmxlV2Vla2x5U2NoZWR1bGUoKSB7XG4gICAgc2NoZWR1bGVUaW1lUm93LmhpZGRlbiA9IGZhbHNlO1xuICAgIHNjaGVkdWxlV2Vla0RheVJvdy5oaWRkZW4gPSBmYWxzZTtcbiAgICBzY2hlZHVsZUN1c3RvbVJvdy5oaWRkZW4gPSB0cnVlO1xuXG4gICAgc2NoZWR1bGVUaW1lSW5wdXQucmVxdWlyZWQgPSB0cnVlO1xuICAgIHNjaGVkdWxlV2Vla0RheUlucHV0LnJlcXVpcmVkID0gdHJ1ZTtcbiAgICBzY2hlZHVsZUN1c3RvbUlucHV0LnJlcXVpcmVkID0gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogRGlzcGxheSBjdXN0b20gc2NoZWR1bGUgZmllbGRzXG4gICAqL1xuICBmdW5jdGlvbiBlbmFibGVDdXN0b21TY2hlZHVsZSgpIHtcbiAgICBzY2hlZHVsZVRpbWVSb3cuaGlkZGVuID0gdHJ1ZTtcbiAgICBzY2hlZHVsZVdlZWtEYXlSb3cuaGlkZGVuID0gdHJ1ZTtcbiAgICBzY2hlZHVsZUN1c3RvbVJvdy5oaWRkZW4gPSBmYWxzZTtcblxuICAgIHNjaGVkdWxlVGltZUlucHV0LnJlcXVpcmVkID0gZmFsc2U7XG4gICAgc2NoZWR1bGVXZWVrRGF5SW5wdXQucmVxdWlyZWQgPSBmYWxzZTtcbiAgICBzY2hlZHVsZUN1c3RvbUlucHV0LnJlcXVpcmVkID0gdHJ1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIaWRlIGFsbCBzY2hlZHVsZSBmaWVsZHMgKG1hbnVhbCB0cmlnZ2VyaW5nIG9wdGlvbilcbiAgICovXG4gIGZ1bmN0aW9uIGVuYWJsZU1hbnVhbFNjaGVkdWxlKCkge1xuICAgIHNjaGVkdWxlVGltZVJvdy5oaWRkZW4gPSB0cnVlO1xuICAgIHNjaGVkdWxlV2Vla0RheVJvdy5oaWRkZW4gPSB0cnVlO1xuICAgIHNjaGVkdWxlQ3VzdG9tUm93LmhpZGRlbiA9IHRydWU7XG5cbiAgICBzY2hlZHVsZVRpbWVJbnB1dC5yZXF1aXJlZCA9IGZhbHNlO1xuICAgIHNjaGVkdWxlV2Vla0RheUlucHV0LnJlcXVpcmVkID0gZmFsc2U7XG4gICAgc2NoZWR1bGVDdXN0b21JbnB1dC5yZXF1aXJlZCA9IGZhbHNlO1xuICB9XG59KSgpO1xuIl0sInNvdXJjZVJvb3QiOiIifQ==