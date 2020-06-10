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
  const scheduleTimezoneInput = document.getElementById("schedule_timezone");

  // detect currently selected schedule type and
  // display appropriate fields
  configureScheduleUI(scheduleTypeInput.value);

  $(scheduleTypeInput).on("change", ($event) => {
    configureScheduleUI($event.target.value);
  });

  /**
   * Configure schedule UI according to the schedule type
   *
   * @param {string} scheduleType type of the schedule
   */
  function configureScheduleUI(scheduleType) {
    switch (scheduleType) {
      case "daily":
        if (isRBAC === true) {
          convertTimesToLocalTimezone(scheduleType);
        }
        enableDailySchedule();
        break;
      case "weekly":
        if (isRBAC === true) {
          convertTimesToLocalTimezone(scheduleType);
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
  /**
   * Gets current timezone from local storage
   * @returns {datetime} either the browser
   *   timezone or manually selected timezone
   */
  function getSelectedTimezone() {
    const manualTz = localStorage.getItem("chosen-timezone");
    const selectedTz = localStorage.getItem("selected-timezone");
    return selectedTz || manualTz;
  }

  function convertTimesToLocalTimezone(scheduleType) {
    scheduleTimezoneInput.value = getSelectedTimezone();
    let convertedTime = convertToTimezone(
      scheduleTimeInput.value,
      scheduleTimezoneInput.value
    );

    scheduleTimeInput.value =
      convertedTime !== "" ? convertedTime.format("HH:mm") : "";
    scheduleTimeInput.dispatchEvent(new Event("change"));

    if (scheduleType === "weekly" && scheduleWeekDayInput.value !== "") {
      const offset = convertedTime.day() - moment(defaultDate).day();
      const currDayOfWeek =
        offset > 0
          ? scheduleWeekDayInput.value + 1
          : scheduleWeekDayInput.value - 1;

      scheduleWeekDayInput.value = currDayOfWeek;
      scheduleWeekDayInput.dispatchEvent(new Event("change"));
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
