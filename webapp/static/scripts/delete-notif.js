// This script enables deleting notification widgets in Bulma
document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        $notification = $delete.parentNode;

        (function(notif) {
            $delete.addEventListener('click', function() {
                console.log(notif);
                notif.parentNode.removeChild(notif);
            });
        })($notification);
    });
});