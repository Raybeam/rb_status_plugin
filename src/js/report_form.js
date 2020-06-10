/* global isRBAC, moment */

(function reportFormSetUp() {
  const defaultDate = "1970-01-01";
  const scheduleTypeInput = document.getElementById("schedule_type");
  const scheduleWeekDayInput = document.getElementById("schedule_week_day");
  const scheduleWeekDayRow =
    scheduleWeekDayInput.closest("tr") ||
    scheduleWeekDayInput.closest(".form-group");
  const scheduleTimeInput = document.getElementById("schedule_time");
  const scheduleTimeRow =
    scheduleTimeInput.closest("tr") || scheduleTimeInput.closest(".form-group");
  const scheduleCustomInput = document.getElementById("schedule_custom");
  const scheduleCustomRow =
    scheduleCustomInput.closest("tr") ||
    scheduleCustomInput.closest(".form-group");

  if (isRBAC === true) {
    var scheduleTimezoneInput = document.getElementById("schedule_timezone");
    var scheduleTimezoneRow =
      scheduleTimezoneInput.closest("tr") ||
      scheduleTimezoneInput.closest(".form-group");
  }
  // detect currently selected schedule type and
  // display appropriate fields
  configureScheduleUI(scheduleTypeInput.value, true);
  $(scheduleTypeInput).on("change", ($event) => {
    configureScheduleUI($event.target.value, false);
  });

  /**
   * Configure schedule UI according to the schedule type
   *
   * @param {string} scheduleType type of the schedule
   * @param {boolean} isInit whether func is trigger by a page
   *    refresh or schedule type change
   */
  function configureScheduleUI(scheduleType, isInit) {
    switch (scheduleType) {
      case "daily":
        if (isRBAC === true) {
          convertTimesToLocalTimezone(isInit, scheduleType);
        }
        enableDailySchedule();
        break;
      case "weekly":
        if (isRBAC === true) {
          convertTimesToLocalTimezone(isInit, scheduleType);
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
   * Converts the specified time to the timezone provided
   *
   * @param {string} time string representing HH:mm string
   * @param {string} tz which timezone to convert to
   */
  function convertToTimezone(time, tz) {
    if (time === "") {
      return "";
    }
    let dateTimeObj = moment.utc(`${defaultDate} ${time}`);
    dateTimeObj.tz(tz);
    return dateTimeObj;
  }

  function offsetDayOfWeek(time) {
    const goForward = moment(defaultDate).add(1, "day");
    const goBackward = moment(defaultDate).subtract(1, "day");

    if (goForward.date() === time.date()) {
      return 1;
    }
    if (goBackward.date() === time.date()) {
      return -1;
    }
    return 0;
  }

  function convertTimesToLocalTimezone(isInit, scheduleType) {
    if (isInit === true) {
      let convertedTime = convertToTimezone(
        scheduleTimeInput.value,
        scheduleTimezoneInput.value
      );

      scheduleTimeInput.value =
        convertedTime !== "" ? convertedTime.format("HH:mm") : "";
      scheduleTimeInput.dispatchEvent(new Event("change"));

      if (scheduleType === "weekly" && scheduleWeekDayInput.value !== "") {
        const offset = offsetDayOfWeek(convertedTime);
        const currWeekDay = moment()
          .day(scheduleWeekDayInput.value)
          .add(offset, "day");
        scheduleWeekDayInput.value = currWeekDay.day();
        scheduleWeekDayInput.dispatchEvent(new Event("change"));
      }
    }
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

    if (isRBAC === true) {
      scheduleTimezoneRow.hidden = false;
      scheduleTimezoneInput.required = true;
    }
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

    if (isRBAC === true) {
      scheduleTimezoneRow.hidden = false;
      scheduleTimezoneInput.required = true;
    }
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

    if (isRBAC === true) {
      scheduleTimezoneRow.hidden = true;
      scheduleTimezoneInput.required = false;
    }
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

    if (isRBAC === true) {
      scheduleTimezoneRow.hidden = true;
      scheduleTimezoneInput.required = false;
    }
  }
})();
