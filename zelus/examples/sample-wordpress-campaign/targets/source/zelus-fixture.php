<?php
/* Synthetic fixture only. */
add_action('wp_ajax_zelus_update_option', 'zelus_update_option');
function zelus_update_option() {
    check_ajax_referer('zelus_nonce');
    update_option('zelus_protected_mode', $_POST['value']);
}
function zelus_render_admin_notice($value) {
    echo $value;
}
