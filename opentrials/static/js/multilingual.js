MULTILINGUAL_FIELDS = {};

$(document).ready(function(){
    if (MULTILINGUAL_FIELDS['available_languages'].length > 2) { // Only when there are more than 2 available languages
        // Prepares multilingual inputs
        $('.multilingual').each(function(){
            // Gets field name
            var f_name = $(this).find('.en').find('input, textarea').attr('name');

            // Creates floating combo to select second language
            var sel = $('<div class="sel"><b>Second language:</b> </div>').prependTo($(this));

            for (var i=0; i<MULTILINGUAL_FIELDS['available_languages'].length; i++) {
                if (MULTILINGUAL_FIELDS['available_languages'][i] !== MULTILINGUAL_FIELDS['display_language']) {
                    var lang = MULTILINGUAL_FIELDS['available_languages'][i].replace(/-[a-z]+$/, '');

                    $('<button type="button" value="'+MULTILINGUAL_FIELDS['available_languages'][i]+'">'+lang+'</button>')
                        .appendTo(sel)
                        .click(function(){
                            var new_lang = $(this).val();
                            $(this).parents('.multilingual').find('.multilingual-value').each(function(){
                                if ($(this).hasClass(MULTILINGUAL_FIELDS['display_language']) || $(this).hasClass(new_lang)) {
                                    $(this).show();
                                } else {
                                    $(this).hide();
                                }
                            });
                        });
                }
            }
        });
    }
});

