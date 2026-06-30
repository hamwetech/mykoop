

        function updateTotal() {
            let qty = parseFloat($('#id_quantity').val()) || 0;
            let price = parseFloat($('#id_unit_price').val()) || 0;
            $('#id_total_price').val((qty * price).toFixed(2));
        }

        // On product change → fetch price
        $('#id_product').change(function() {
            let productId = $(this).val();

            if (!productId) return;

            $.ajax({
                url: '/get-product-price/' + productId + '/',
                type: 'GET',
                success: function(response) {
                    $('#id_unit_price').val(response.price);
                    updateTotal();
                }
            });
        });

        // On quantity change → update total
        $('#id_quantity, #id_unit_price').on('keyup change', function() {
            updateTotal();
        });