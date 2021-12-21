var KTBootstrapDaterangepicker = function () {

    var demos = function () {
        $('#kt_daterangepicker_1, #kt_daterangepicker_1_modal').daterangepicker({
            buttonClasses: ' btn',
            applyClass: 'btn-primary',
            cancelClass: 'btn-secondary'
        });
    };

    return {
        init: function () {
            demos();
        }
    };
}();

jQuery(document).ready(function () {
    KTBootstrapDaterangepicker.init();
});