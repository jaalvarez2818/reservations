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
                    } else {
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
                                if (data.error) {
                                    toastr.error(data.message);
                                    wizardObj.stop();
                                } else {
                                    if (!data.availability) {
                                        toastr.error(data.message);
                                        wizardObj.stop();
                                    } else {
                                        $('#guests').prop('max', data.max);
                                        $('#room_typology_abstract').text($('#room_typology option:selected').text());
                                        $('#date_range_abstract').text($('#kt_daterangepicker_1').val());
                                    }
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
                                toastr.error(data.message);
                                wizardObj.stop();
                            } else {
                                $('#guests_abstract').text($('#guests').val());
                                $('#name_abstract').text($('#name').val());
                                $('#email_abstract').text($('#email').val());
                                $('#phone_abstract').text($('#phone').val());
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
                toastr.error('Please, correct the errors.');
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

                var $form = $('#kt_form');

                var url = $form.prop('action');

                $.ajax({
                    url: url,
                    data: $form.serialize(),
                    type: 'POST',
                    async: false,
                    success: function (data) {
                        if (data.error) {
                            toastr.error(data.message);
                        } else {
                            window.location.href = data.redirect_to;
                        }
                        KTApp.unprogress(btn);
                    },
                    error: function (data) {
                        toastr.error('Error de servidor.');
                        KTApp.unprogress(btn);
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
