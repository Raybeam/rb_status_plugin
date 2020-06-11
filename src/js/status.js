/* global rbStatusContent, isoDateToTimeEl */

setReportsTimes(rbStatusContent);

/**
 * Display dates in a airflow defined timezone and format.
 *
 * @param {object} content Status page content from the template
 */
function setReportsTimes(content) {
  // update summary status updated datetime
  const summaryUpdatedEl = document.querySelector(".report-datetime-header");
  if (content.summary.updated) {
    summaryUpdatedEl.innerHTML = "";
    summaryUpdatedEl.append(
      isoDateToTimeEl(content.summary.updated, { title: false })
    );
  }

  // update reports updated datetime
  for (const report of content.reports) {
    const updatedElSelector = `#report-${report.report_title_id}-heading .report-datetime`;
    const updatedEl = document.querySelector(updatedElSelector);
    updatedEl.innerHTML = "";
    updatedEl.append(isoDateToTimeEl(report.updated, { title: false }));
  }
}
