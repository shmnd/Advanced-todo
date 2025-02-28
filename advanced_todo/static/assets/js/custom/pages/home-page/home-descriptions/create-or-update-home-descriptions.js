"use strict";

// Class definition
let MCUpdateOrCreateProperty = function () {

let validator;

let form;
const handleSubmit = () => {
    // Get elements
    form = document.getElementById('create-or-update-company-profile-form');
    const submitButton = document.getElementById('create-or-update-company-profile-submit');

    validator = FormValidation.formValidation(
        
        form,
        {
            fields: {
                'descriptions_one': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'descriptions_two': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'descriptions_three': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'descriptions_four': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'descriptions_five': {
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
            validator.validate().then(function (status) {
                
                console.log('validated!');
                submitButton.setAttribute('data-kt-indicator', 'on');

                // Disable button to avoid multiple click
                submitButton.disabled = true;

                if (status == 'Valid') {

                    // Handle submit button
                    e.preventDefault();
                    const btn = document.getElementById('create-or-update-company-profile-submit');
                    const text = document.getElementById('banner-loader-text');
                    btn.disabled = true;
                    btn.style.display = 'none';
                    text.style.display = 'block';
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
MCUpdateOrCreateProperty.init();
});



