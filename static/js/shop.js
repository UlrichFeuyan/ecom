(function ($) {
  "use strict";

  var filterProducts = function () {
    // Hàm xử lý lọc sản phẩm
    var applyFilter = function () {
      var selectedColors = [];
      var selectedSizes = [];
      var selectedMinPrice = $(".range-min").val() ? parseFloat($(".range-min").val()) : 0;
      var selectedMaxPrice = $(".range-max").val() ? parseFloat($(".range-max").val()) : 300;
  
      // Cập nhật giá trị hiển thị cho giá trị min/max price
      $(".min-price").text(`${selectedMinPrice}`);
      $(".max-price").text(`${selectedMaxPrice}`);
  
      // Lấy tất cả các bộ lọc màu sắc đã chọn
      $(".tf-check-color:checked").each(function () {
        selectedColors.push($(this).val());
      });
  
      // Lấy tất cả các bộ lọc kích thước đã chọn
      $(".tf-check-size:checked").each(function () {
        selectedSizes.push($(this).val());
      });
  
      var visibleProductCount = 0;  // Đếm số lượng sản phẩm hiển thị
  
      // Lặp qua tất cả các thẻ sản phẩm
      $(".card-product").each(function () {
        var categoryColor = $(this).data("color");
        var categorySize = $(this).data("size");
        var productPrice = parseFloat($(this)?.data("price"));
  
        var showByColor = selectedColors.length === 0 || selectedColors.some(filter => (categoryColor || "").split(" ").includes(filter));
        var showBySize = selectedSizes.length === 0 || selectedSizes.some(filter => (categorySize || "").split(" ").includes(filter));
        var showByPrice = productPrice >= selectedMinPrice && productPrice <= selectedMaxPrice;
  
        // Hiển thị sản phẩm nếu nó đáp ứng tất cả các điều kiện
        if (showByColor && showBySize && showByPrice) {
          $(this).show();
          visibleProductCount++;  // Tăng bộ đếm sản phẩm hiển thị
        } else {
          $(this).hide();
        }
      });
  
      // Hiển thị hoặc ẩn phân trang dựa trên số lượng sản phẩm hiển thị
      if (visibleProductCount >= 12) {
        $(".tf-pagination-btn").show();
      } else {
        $(".tf-pagination-btn").hide();
      }
  
      // Hiển thị thông báo "Không có sản phẩm" nếu không có sản phẩm nào hiển thị
      if (visibleProductCount === 0) {
        if (!$(".wrapper-control-shop").find("h4").length) {
          $(".wrapper-control-shop").append('<h4 class="text-center">No Products</h4>');
        }
      } else {
        $(".wrapper-control-shop").find("h4").remove();
      }
  
      // Hiển thị số lượng sản phẩm được tìm thấy
      if (visibleProductCount > 0) {
        if ($("#product-count").length === 0) {
          $(".meta-filter-shop").append(`<p id="product-count" class="text-2">${visibleProductCount} product(s) found</p>`);
        } else {
          $("#product-count").text(`${visibleProductCount} product(s) found`);
        }
      } else {
        $("#product-count").remove(); 
      }
  
      if (selectedColors.length > 0 || selectedSizes.length > 0 || selectedMinPrice > 0 || selectedMaxPrice < 300) {
        if ($("#clear-filters").length === 0) {
          $(".meta-filter-shop").append('<button id="clear-filters" class="tf-btn style-3 btn-fill animate-hover-btn">Clear Filters</button>');
          $("#clear-filters").on("click", function () {
            $(".tf-check-color, .tf-check-size").prop("checked", false); 
            $(".range-min").val(0);
            $(".range-max").val(300);
            $(".min-price").text('0');
            $(".max-price").text('300');
            $(".progress-price").css("left",'0%');
            $(".progress-price").css("right",'0%');
            applyFilter();
            $(this).remove();
            $("#product-count").remove();
          });
        }
      } else {
        // Nếu không có bộ lọc nào được chọn, ẩn nút "Clear"
        $("#clear-filters").remove();
        $("#product-count").remove(); // Xóa product count
      }
    };
    // Sự kiện thay đổi checkbox và range input để lọc sản phẩm
    $("input.tf-check-color, input.tf-check-size, .range-min, .range-max").on("change", applyFilter);
  
  };
  
  

  


  $(function () {
    filterProducts();
  });
})(jQuery);
