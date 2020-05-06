(function reportFormSetUp() {
  const scheduleTypeInput = document.getElementById("schedule_type");
  const scheduleWeekDayRow = document
    .getElementById("schedule_week_day")
    .closest("tr");
  const scheduleTime = document.getElementById("schedule_time").closest("tr");
  const scheduleCustomRow = document
    .getElementById("schedule_custom")
    .closest("tr");

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
      default:
        break;
    }
  }

  /**
   * Display daily schedule fields
   */
  function enableDailySchedule() {
    scheduleTime.hidden = false;
    scheduleWeekDayRow.hidden = true;
    scheduleCustomRow.hidden = true;
  }

  /**
   * Display weekly schedule fields
   */
  function enableWeeklySchedule() {
    scheduleTime.hidden = false;
    scheduleWeekDayRow.hidden = false;
    scheduleCustomRow.hidden = true;
  }

  /**
   * Display custom schedule fields
   */
  function enableCustomSchedule() {
    scheduleTime.hidden = true;
    scheduleWeekDayRow.hidden = true;
    scheduleCustomRow.hidden = false;
  }
})();
