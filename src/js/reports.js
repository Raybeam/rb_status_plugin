/*global postAsForm */

// expose lumen API
window.lumen = {
  confirmDeleteReport,
  triggerReportStartPause,
};

/**
 * Delete report.
 * Ask user for confirmation prior to sending a request.
 *
 * @param {HTMLElement} link html element the function is called on
 */
// eslint-disable-next-line no-unused-vars
function confirmDeleteReport(link) {
  const reportName = link.dataset.reportName;
  const answer = confirm(
    `Are you sure you want to delete ${reportName} report`
  );
  if (answer) {
    postAsForm(link.href, {
      report_name: reportName,
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
  let url = input.dataset.pauseUrl;
  const reportName = encodeURIComponent(input.dataset.reportName);
  const isPaused = input.checked;

  url = `${url}?report_name=${reportName}&is_paused=${isPaused}`;
  const data = new FormData();
  data.append("csrf_token", csrfToken);

  fetch(url, {
    method: "POST",
    body: data,
  }).then((response) => {
    if (!response.ok) {
      $(input).data("bs.toggle").off(!isPaused);
    }
  });
}
