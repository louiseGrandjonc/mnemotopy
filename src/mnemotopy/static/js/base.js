'use strict';

(function() {
    $(document).ready(function() {
        $(document).on('click', '.header-nav__lang', function(e){
            e.preventDefault();
            var lang = $(this).data('lang'),
                form = $(this).parent().find('form:first');

            $('#id_language').val(lang);
            form.submit();
        });
    });

})()
