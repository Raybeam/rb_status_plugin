/* global isRBAC, moment */

(function reportFormSetUp() {
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

  // read time and weekDay while it's in UTC
  const time = scheduleTimeInput.value;
  const weekDay = scheduleWeekDayInput.value;
  const timeZone = getClientTimezone();

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
    return (
      localStorage.getItem("selected-timezone") ||
      localStorage.getItem("chosen-timezone")
    );
  }

  /**
   * Convert schedule from UTC to client timezone
   */
  function convertToClientTimezone() {
    if (!time) {
      return;
    }

    const dateTimeUTC = moment.utc(time, "HH:mm");
    if (weekDay) {
      dateTimeUTC.day(Number(weekDay));
    }

    const dateTimeInClientTZ = dateTimeUTC.clone().tz(timeZone);
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
