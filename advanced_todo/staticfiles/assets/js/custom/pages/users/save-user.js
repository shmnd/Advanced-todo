"use strict";

// Class definition
const MCUpdateOrCreateUser = function () {
    
    const handleSubmit = () => {
        let validator;
        // Get elements
        const form = document.getElementById('create-or-update-user-form');
        const submitButton = document.getElementById('create-or-update-user-submit');
        let email_value = false
        


        const strongPassword = function () {
            $("#email_id").keyup(function(){
                let email = document.getElementById("email_id").value;
                $.post(`${api_config.email_check}`, { email: email }, function(data, status, xhr) {
                    
                    if(data.result == true){
                        email_value = true
                    }else
                    {
                        email_value = false
                    }
    
                });
            })
            return email_value
        }   
        FormValidation.validators.checkPassword = strongPassword();
        
        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    'first_name': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'last_name': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    'email': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                       
                        }
                        
                    },
                    'password': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'phone': {
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


        submitButton.addEventListener('click', e => {
            e.preventDefault();
            // Validate form before submit
            if (validator) {
                console.log(strongPassword())
                validator.validate().then(function (status) {
                    console.log('validated!');
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    if (status == 'Valid') {
                        // Handle submit button
                        e.preventDefault();
                        submitButton.setAttribute('data-kt-indicator', 'on');
                        // Disable submit button whilst loading
                        submitButton.disabled = true;
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable submit button after loading
                        submitButton.disabled = false;

                        // Redirect to customers list page
                        form.submit();
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        Swal.fire({
                            html: "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            }
        });
    }

    
    // Public methods
    return {
        init: function () {
            handleSubmit();
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateUser.init();
});
