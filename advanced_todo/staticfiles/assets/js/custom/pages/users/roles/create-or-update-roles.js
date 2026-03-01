"use strict";



// Class definition
const MCUpdateOrCreateRoles = function () {

    let validator;
    let form;


    const handleSubmit = () => {
        

        // Get elements
        form = document.getElementById('create-or-update-role-form');
        const submitButton = document.getElementById('create-or-update-role-submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    role_name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            // Add a custom validator for unique role name
                            regexp: {
                                regexp: /^(?=.*[A-Za-z])[A-Za-z\s]+$/,
                                message: 'Only characters are allowed, and at least one non-space character is required'
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


        submitButton.addEventListener('click', async (e) => {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                try {
                    const status = await validator.validate();

                    const permissionIdsOutput = document.querySelector(`[data-control-permissions="id"]`);
                    const permissionIds = getSelectedPermissionIds();

                    permissionIdsOutput.value = JSON.stringify(permissionIds);

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

    const getSelectedPermissionIds = () => {
        const selected_nodes = $('#_jstree_checkable').jstree().get_selected(true);
        const permissionIds = [];

        selected_nodes.forEach(d => {
            if (typeof d.a_attr.permission_id !== 'undefined') {
                permissionIds.push(d.a_attr.permission_id);
            }
        });

        return permissionIds;
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

    const handlePermissionTree = () => {
        $.post(`${api_config.generate_permission_tree}`, { role_id: `${api_config.role_id}` }, function (data, status, xhr) {
            console.log(data.data);
            if (data.status_code === 200) {
                $('#_jstree_checkable').jstree({
                    'plugins': ["wholerow", "checkbox", "types", "changed"],
                    'core': {
                        "themes": {
                            "responsive": false
                        },
                        'data': data.data
                    },
                    "types": {
                        "default": {
                            "icon": "fa fa-folder text-primary"
                        },
                        "file": {
                            "icon": "fa fa-file text-primary"
                        }
                    },
                });
            }
        }).done(function () {
            console.log('Request done!');
        }).fail(function (jqxhr, settings, ex) {
            console.log('failed, ' + ex);
        });
    };

    // Public methods
    return {
        init: function () {
            handleSubmit();
            handlePermissionTree();
        }
    };
}();

window.addEventListener('load', function () {
    const loader = document.querySelector('.loader-wrapper');
    loader.style.display = 'none';
});

// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateRoles.init();
});

