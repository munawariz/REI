function confirmationAlert(title, confirmlink){
	Swal.fire({
		title: title,
		showDenyButton: true,
		confirmButtonText: `Ya`,
		denyButtonText: `Tidak`,
	  }).then((result) => {
		if (result.isConfirmed) {
		  location.href = confirmlink
		}
	})
}

function formAlert(title, form){
    Swal.fire({
        title: title,
        html: form,
        showCloseButton: true,
        showCancelButton: true,
		preConfirm: () => {
			try{
				$('#sweetalertForm input, #sweetalertForm select').each(
					function(index){  
						var input = $(this);
						if (!input.val() && input.attr('required')){
							throw new Error("Silahkan Lengkapi Form Terlebih Dahulu")
						}
					}
				);
			}catch (error){
				Swal.showValidationMessage(
					`${error}`
				)
			}
		},
        
    }).then((result) => {
		if (result.isConfirmed) {
		  document.sweetalertForm.submit()
		}
    })
}