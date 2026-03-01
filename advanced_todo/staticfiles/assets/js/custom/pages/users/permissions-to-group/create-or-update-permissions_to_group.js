"use strict";



// Class definition
const MCUpdateOrCreateSupplier = function () {

    let validator;
    let form;

    let categoryElement, brandElement;

    const handleSubmit = () => {
        

        // Get elements
        form = document.getElementById('create-or-update-permissions_to_group-form');
        const submitButton = document.getElementById('create-or-update-permissions_to_group-submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    group_obj_name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    permissions: {
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

            categoryElement = document.querySelector('[data-control-select-option="category"]')
            brandElement = document.querySelector('[data-control-select-option="brand"]')

            handleSubmit();
            
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateSupplier.init();
});




function generateBase64encodedURL(src, callback){
    let image = new Image();
    image.crossOrigin = 'Anonymous';
    image.onload = function(){
      let canvas = document.createElement('canvas');
      let context = canvas.getContext('2d');
      //canvas.height = this.naturalHeight;
      canvas.height = 140;
      canvas.width = 140;
      //canvas.width = this.naturalWidth;
      context.drawImage(this, 0, 0,140,140);
      let dataURL = canvas.toDataURL('image/jpeg');
      callback(dataURL);
    };
    image.src = src;
}
