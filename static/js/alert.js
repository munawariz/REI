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
        icon: 'info',
        html: form,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: true,
        
    }).then((result) => {
		if (result.isConfirmed) {
		  document.sweetalertForm.submit()
		}
    })
}