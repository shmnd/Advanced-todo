
function previewImage(event) {
    let logoPreview = document.getElementById('logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}


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
                'designation': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'min_exp': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'education': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'city': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'company': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'max_exp': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'category': {
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


    submitButton.addEventListener('click', async e => {
        e.preventDefault();
    
        // Validate form before submit
        
        if (validator) {
            try {
                const status = await validator.validate();
                //Project Aim
                let responsibilities = [];
                // Collect repeater items data
                const responsibilitiesContainer = document.getElementById('features');
                const responsibilitiesrepeaterItems = responsibilitiesContainer.querySelectorAll('[data-repeater-item]');
                // Iterate through the repeater items and extract values
                responsibilitiesrepeaterItems.forEach((item, index) => {
                    // Select the <input> element inside the current repeater item
                    const inputElement = item.querySelector('[name^="features"][name$="[name]"]');
                
                    // Extract the input value
                    const inputValue = inputElement ? inputElement.value.trim() : null;
                
                    // Check if inputValue is not empty before appending
                    if (inputValue !== null && inputValue !== "") {
                        responsibilities.push(inputValue);
                    }
                });
                //Project Aim End
                
                //Problem Statement
                let skills = [];
                // Collect repeater items data
                const skillsContainer = document.getElementById('subfeatures');
                const skillsRepeaterItems = skillsContainer.querySelectorAll('[data-repeater-item]');
                // Iterate through the repeater items and extract values
                skillsRepeaterItems.forEach((item, index) => {
                    // Select the <input> element inside the current repeater item
                    const inputElement = item.querySelector('[name^="subfeatures"][name$="[subname]"]');
                    // Extract the input value
                    const inputValue = inputElement ? inputElement.value.trim() : null;
                
                    // Check if inputValue is not empty before appending
                    if (inputValue !== null && inputValue !== "") {
                        skills.push(inputValue);
                    }
                });
                //Problem Statement End

                const formData = new FormData();    
                formData.append('instance_id', document.querySelector('[name="instance_id"]').value);
                formData.append('designation', document.querySelector('[name="designation"]').value);
                formData.append('min_exp', document.querySelector('[name="min_exp"]').value);
                formData.append('max_exp', document.querySelector('[name="max_exp"]').value);
                formData.append('tags', document.querySelector('[name="tags"]').value);
                formData.append('category', document.querySelector('[name="category"]').value);
                formData.append('company', document.querySelector('[name="company"]').value);
                formData.append('education', document.querySelector('[name="education"]').value);
                formData.append('city', document.querySelector('[name="city"]').value);
                formData.append('description', CKEDITOR.instances.mytextarea.getData());
                // formData.append('description', document.querySelector('[name="description"]').value);
                
                formData.append('responsibilities',JSON.stringify(responsibilities))
                formData.append('skills',JSON.stringify(skills))

                submitButton.setAttribute('data-kt-indicator', 'on');
                submitButton.disabled = true;
    
                if (status === 'Valid') {
                    const btn = document.getElementById('create-or-update-company-profile-submit');
                    const loadingBtn = document.getElementById('banner-loader-text');
    
                    btn.style.display = 'none';
                    loadingBtn.style.display = 'inline-block';
    
                    const response = await fetch(api_config.create_or_update_from, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': api_config.csrfmiddlewaretoken,
                        },
                        body: formData,
                    });
    
                    const data = await response.json();
    
                    if (data.status === 200) {
                        const redirectUrl = form.getAttribute('data-redirect-url');
                        if (redirectUrl) {
                            location.href = redirectUrl;
                        }
                    }
                     else {
                        // Handle other cases if needed
                        submitButton.removeAttribute('data-kt-indicator');
                        btn.style.display = 'inline-block';
                        loadingBtn.style.display = 'none';
                        submitButton.disabled = false;
    
                        Swal.fire({
                            html: data.message || "please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                } else {
                    submitButton.removeAttribute('data-kt-indicator');
                    submitButton.disabled = false;
    
                    Swal.fire({
                        html: data.message || "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    });
                }
            } catch (error) {
                console.error('Error during validation:', error);
            }
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



