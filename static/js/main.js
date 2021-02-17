var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)})
$(document).ready(function() {
    $(document.body).on("click", "tr[data-href]", function () {
        window.location.href = this.dataset.href;
    });
});