"use strict";

var KTWizard1 = function () {
    var wizardEl;
    var formEl;
    var validator;
    var wizard;

    var initWizard = function () {
        wizard = new KTWizard('kt_wizard_v1', {
            startStep: 1
        });

        wizard.on('beforeNext', function (wizardObj) {
            if (validator.form() !== true) {
                wizardObj.stop();
            }
            switch (wizardObj.getStep()) {
                case 1:
                    var range = $('#kt_daterangepicker_1').val().split(' - ');
                    if (range[0] === range[1]) {
                        toastr.error('Debe reservar al menos por un día.');
                        wizardObj.stop();
                    }
                    else {
                        $.ajax({
                            url: '/availability',
                            data: {
                                room_typology: $('#room_typology').val(),
                                start_date: range[0],
                                end_date: range[1]
                            },
                            type: 'GET',
                            async: false,
                            success: function (data) {
                                if (!data.availability) {
                                    toastr.error('No tenemos habitaciones disponibles.');
                                    wizardObj.stop();
                                } else {
                                    $('#guests').prop('max', data.max);
                                }
                            },
                            error: function (data) {
                                toastr.error('Error de servidor.');
                            }
                        });
                    }
                    break;
                case 2:
                    $.ajax({
                        url: '/check_person',
                        data: {
                            email: $('#email').val()
                        },
                        type: 'GET',
                        async: false,
                        success: function (data) {
                            if (!data.can_reservate) {
                                toastr.error('Usted no puede reservar habitaciones.');
                                wizardObj.stop();
                            }
                        },
                        error: function (data) {
                            toastr.error('Error de servidor.');
                        }
                    });
                    break;
            }
        });

        wizard.on('change', function (wizard) {
            setTimeout(function () {
                KTUtil.scrollTop();
            }, 500);
        });
    };

    var initValidation = function () {
        validator = formEl.validate({
            ignore: ":hidden",

            rules: {
                //= Step 1
                room_typology: {
                    required: true
                },
                kt_daterangepicker_1: {
                    required: true
                },

                //= Step 2
                guests: {
                    required: true
                },
                name: {
                    required: true
                },
                email: {
                    required: true
                },
                phone: {
                    required: true
                }
            },

            invalidHandler: function (event, validator) {
                KTUtil.scrollTop();
                toastr.error('No tenemos habitaciones disponibles.');
            },

            submitHandler: function (form) {

            }
        });
    };

    var initSubmit = function () {
        var btn = formEl.find('[data-ktwizard-type="action-submit"]');

        btn.on('click', function (e) {
            e.preventDefault();

            if (validator.form()) {
                KTApp.progress(btn);

                formEl.ajaxSubmit({
                    success: function () {
                        KTApp.unprogress(btn);
                        //KTApp.unblock(formEl);

                        swal.fire({
                            "title": "",
                            "text": "The application has been successfully submitted!",
                            "type": "success",
                            "confirmButtonClass": "btn btn-secondary"
                        });
                    }
                });
            }
        });
    };

    return {
        // public functions
        init: function () {
            wizardEl = KTUtil.get('kt_wizard_v1');
            formEl = $('#kt_form');

            initWizard();
            initValidation();
            initSubmit();
        }
    };
}();

jQuery(document).ready(function () {
    KTWizard1.init();
});