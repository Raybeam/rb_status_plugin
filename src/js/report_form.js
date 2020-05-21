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
        enableDailySchedule();
        break;
      case "weekly":
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
