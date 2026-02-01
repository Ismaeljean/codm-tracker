(function($) {
    $(document).ready(function() {
        // Masquer/afficher type_tournoi selon le mode
        function toggleTypeTournoi() {
            var mode = $('#id_mode').val();
            var typeField = $('.field-type_tournoi');
            
            if (mode === 'MJ') {
                // Multijoueur : masquer type_tournoi
                typeField.hide();
                $('#id_type_tournoi').val('').prop('required', false);
            } else if (mode === 'BR') {
                // Battle Royale : afficher type_tournoi
                typeField.show();
                $('#id_type_tournoi').prop('required', true);
            }
        }
        
        // Au chargement de la page
        toggleTypeTournoi();
        
        // Quand le mode change
        $('#id_mode').on('change', function() {
            toggleTypeTournoi();
        });
    });
})(django.jQuery);
