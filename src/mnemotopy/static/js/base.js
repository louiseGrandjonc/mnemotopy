'use strict';

(function() {
    $(document).ready(function() {
        $(document).on('change', '#id_mp_lang', function() {
            console.log($(this).parents('form:first'));
            $(this).parents('form:first').submit();
        });
    });
})()
