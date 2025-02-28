"use strict";



// Class definition
const MCUpdateOrCreateGroup = function () {

    let validator;
    let form;


    const handleSubmit = () => {
        

        // Get elements
        form = document.getElementById('create-or-update-group-form');
        const submitButton = document.getElementById('create-or-update-roles-group-submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    group_name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^(?=.*[A-Za-z])[A-Za-z\s]+$/,
                                message: 'Only characters are allowed, and at least one non-space character is required'
                            }
                        }
                    },
                    role: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },              
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        );


        submitButton.addEventListener('click', async (e) => {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                try {
                    const status = await validator.validate();

                    console.log('validated!');

                    submitButton.setAttribute('data-kt-indicator', 'on');
                    submitButton.disabled = true;

                    if (status === 'Valid') {
                        // Simulate an asynchronous operation (e.g., API call) with setTimeout
                        setTimeout(() => {
                            form.submit();
                        }, 1000); // Adjust the delay as needed
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');
                        submitButton.disabled = false;
                        displayErrorAlert();
                    }
                } catch (error) {
                    console.error('Validation error:', error);
                }
            }
        });
    };

    const displayErrorAlert = () => {
        Swal.fire({
            html: "Sorry, looks like there are some errors detected, please try again.",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });
    };

    // Public methods
    return {
        init: function () {
            handleSubmit();
        }
    };
}();
window.addEventListener('load', function () {
    const loader = document.querySelector('.loader-wrapper');
    loader.style.display = 'none';
});

// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateGroup.init();
});




