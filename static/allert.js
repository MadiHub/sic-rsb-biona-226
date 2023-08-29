

// END

// LOGIN ALLERT
 const urlParams = new URLSearchParams(window.location.search);
 const successParam = urlParams.get('success');

 // If success parameter is 1, show success alert
 if (successParam === '1') {
     Swal.fire({
         icon: 'success',
         title: 'Success!',
         text: 'You have successfully logged in.',
         confirmButtonColor: '#3085d6',
         confirmButtonText: 'OK'
     }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = '/'; // Redirect to login page
        }
      });
      // Remove the 'success' parameter from the URL
      var url = new URL(window.location.href);
      url.searchParams.delete('success');
      history.replaceState(null, '', url);
 }

//  Logout
function confirmLogout() {
  Swal.fire({
  icon: 'warning',
  title: 'Peringatan !',
  text: 'Apa Anda Yakin Ingin Logout Akun ?',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Ya, logout'
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = 'logout';
    }
  });
}