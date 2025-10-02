    // Login Section
    function openLoginModal() {
        document.getElementById('auth-modal').classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        switchAuthTab('login');
    }

        const leftSection = document.querySelector(".left-section");
    if (leftSection) {
        leftSection.style.background = "linear-gradient(135deg, var(--shipzoid-navy), var(--shipzoid-navy-dark))";
    }

    // Close modal
    function closeAuthModal() {
        document.getElementById('auth-modal').classList.add('hidden');
        document.body.style.overflow = '';
    }

    // Switch between login & signup tabs
    function switchAuthTab(tab, evt = null) {
        document.querySelectorAll('.auth-tab').forEach(btn => {
            btn.classList.remove('border-b-2', 'border-shipzoid-teal', 'text-shipzoid-teal', 'font-semibold');
            btn.classList.add('text-gray-500');
        });

        const activeTab = document.querySelector(`.auth-tab:nth-child(${tab === 'login' ? 1 : 2})`);
        if (activeTab) {
            activeTab.classList.remove('text-gray-500');
            activeTab.classList.add('border-b-2', 'border-shipzoid-teal', 'text-shipzoid-teal', 'font-semibold');
        }

        document.querySelectorAll('.auth-form').forEach(f => f.classList.add('hidden'));
        document.getElementById(tab + '-form').classList.remove('hidden');
    }

    // Toggle password visibility
    function togglePassword(inputId) {
        const input = document.getElementById(inputId);
        const icon = input.parentElement.querySelector('i');
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }

    // Validation helpers
    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function validatePhone(phone) {
        return /^[+]?[\d\s-()]+$/.test(phone) && phone.replace(/\D/g, '').length >= 10;
    }

    function validatePassword(password) {
        return password.length >= 8;
    }

    function showFieldError(fieldId, message) {
        const errorDiv = document.getElementById(fieldId + '-error');
        if (errorDiv) errorDiv.innerHTML = `<i class="fas fa-exclamation-circle mr-1"></i>${message}`;
    }

    function clearFieldError(fieldId) {
        const errorDiv = document.getElementById(fieldId + '-error');
        if (errorDiv) errorDiv.innerHTML = '';
    }

    // Login form handler
    function handleLogin(event) {
        event.preventDefault();

        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value;
        const btn = document.getElementById('login-btn');

        clearFieldError('login-email');
        clearFieldError('login-password');

        let hasErrors = false;

        if (!email) {
            showFieldError('login-email', 'Email or phone is required');
            hasErrors = true;
        } else if (!validateEmail(email) && !validatePhone(email)) {
            showFieldError('login-email', 'Please enter a valid email or phone number');
            hasErrors = true;
        }

        if (!password) {
            showFieldError('login-password', 'Password is required');
            hasErrors = true;
        }

        if (hasErrors) return;

        // Loading
        btn.querySelector('span').classList.add('hidden');
        btn.querySelector('.loading').classList.remove('hidden');
        btn.disabled = true;

        // Simulated API
        setTimeout(() => {
            btn.querySelector('span').classList.remove('hidden');
            btn.querySelector('.loading').classList.add('hidden');
            btn.disabled = false;
            alert('Login successful! Welcome back to Shipzoid.');
            closeAuthModal();
            updateUserState(email);
        }, 1500);
    }

    // Signup form handler
    function handleSignup(event) {
        event.preventDefault();

        const name = document.getElementById('signup-name').value.trim();
        const email = document.getElementById('signup-email').value.trim();
        const phone = document.getElementById('signup-phone').value.trim();
        const password = document.getElementById('signup-password').value;
        const confirmPassword = document.getElementById('signup-confirm-password').value;
        const btn = document.getElementById('signup-btn');

        ['signup-name', 'signup-email', 'signup-phone', 'signup-password', 'signup-confirm-password'].forEach(clearFieldError);

        let hasErrors = false;

        if (!name) {
            showFieldError('signup-name', 'Full name is required');
            hasErrors = true;
        }

        if (!email) {
            showFieldError('signup-email', 'Email is required');
            hasErrors = true;
        } else if (!validateEmail(email)) {
            showFieldError('signup-email', 'Please enter a valid email address');
            hasErrors = true;
        }

        if (!phone) {
            showFieldError('signup-phone', 'Phone number is required');
            hasErrors = true;
        } else if (!validatePhone(phone)) {
            showFieldError('signup-phone', 'Please enter a valid phone number');
            hasErrors = true;
        }

        if (!password) {
            showFieldError('signup-password', 'Password is required');
            hasErrors = true;
        } else if (!validatePassword(password)) {
            showFieldError('signup-password', 'Password must be at least 8 characters long');
            hasErrors = true;
        }

        if (!confirmPassword) {
            showFieldError('signup-confirm-password', 'Please confirm your password');
            hasErrors = true;
        } else if (password !== confirmPassword) {
            showFieldError('signup-confirm-password', 'Passwords do not match');
            hasErrors = true;
        }

        if (hasErrors) return;

        // Loading
        btn.querySelector('span').classList.add('hidden');
        btn.querySelector('.loading').classList.remove('hidden');
        btn.disabled = true;

        // Simulated API
        setTimeout(() => {
            btn.querySelector('span').classList.remove('hidden');
            btn.querySelector('.loading').classList.add('hidden');
            btn.disabled = false;
            alert('Account created successfully! Welcome to Shipzoid.');
            closeAuthModal();
            updateUserState(email);
        }, 1500);
    }

    // Update header after login/signup
    function updateUserState(email) {
        const accountBtn = document.getElementById('open-auth-modal');
        accountBtn.innerHTML = `<i class="fas fa-user-circle"></i><span>${email.split('@')[0]}</span>`;
        accountBtn.onclick = () => alert('Profile management coming soon!');
    }




            let cartItems = [];

            async function fetchCart() {
                showLoader(); // show shimmer while waiting
                try {
                    const res = await fetch("/home/get-cart-items/");

                    // Check for login or other errors
                    if (!res.ok) {
                        const errorData = await res.json();
                        showLoginError(errorData.message || "Please login to continue.");
                        return;
                    }

                    const data = await res.json();
                    cartItems = data.cart;
                    renderCart();

                } catch (error) {
                    console.error("Error fetching cart:", error);
                    document.getElementById("cart-content").innerHTML = `
                        <div class="text-center py-8 text-red-500">
                            Failed to load cart. Please try again.
                        </div>`;
                }
            }


                function showLoader() {
                    const cartContent = document.getElementById("cart-content");
                    cartContent.innerHTML = "";

                    for (let i = 0; i < 3; i++) { // 3 placeholder items
                        const skeleton = document.createElement("div");
                        skeleton.className = "grid grid-cols-1 sm:grid-cols-3 items-center gap-4 border rounded-lg p-4 shadow-sm animate-pulse";

                        skeleton.innerHTML = `
                            <!-- Image skeleton -->
                            <div class="flex justify-center sm:justify-start">
                                <div class="w-24 h-24 bg-gray-200 rounded-lg"></div>
                            </div>

                            <!-- Details skeleton -->
                            <div class="flex-1 space-y-2">
                                <div class="w-3/4 h-5 bg-gray-200 rounded"></div>
                                <div class="w-1/2 h-4 bg-gray-200 rounded"></div>
                                <div class="flex items-center gap-3 mt-2">
                                    <div class="w-16 h-4 bg-gray-200 rounded"></div>
                                    <div class="flex items-center gap-2">
                                        <div class="w-6 h-6 bg-gray-200 rounded"></div>
                                        <div class="w-6 h-6 bg-gray-200 rounded"></div>
                                    </div>
                                </div>
                            </div>

                            <!-- Total + remove skeleton -->
                            <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2">
                                <div class="w-12 h-5 bg-gray-200 rounded"></div>
                                <div class="w-6 h-6 bg-gray-200 rounded-full"></div>
                            </div>
                        `;
                        cartContent.appendChild(skeleton);
                    }
                }


            function showLoginError(message) {
                const cartContent = document.getElementById("cart-content");
                const cartFooter = document.getElementById("cart-footer");
                cartContent.innerHTML = `
                    <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
                        <div class="w-24 h-24 bg-gray-100 flex items-center justify-center rounded-full shadow-md">
                            <i class="fas fa-user-lock text-gray-400 text-4xl"></i>
                        </div>
                        <h3 class="mt-4 text-lg font-semibold text-gray-700">${message}</h3>
                    </div>
                `;

                // Reset totals and counts
                cartFooter.classList.add("hidden");
                document.getElementById("cart-total").textContent = 0;
                document.getElementById("cart-count").textContent = 0;
            }


            function renderCart() {
                const cartContent = document.getElementById("cart-content");
                const cartFooter = document.getElementById("cart-footer");
                cartContent.innerHTML = ""; // clear previous
                let total = 0;

                if (cartItems.length === 0) {
                    // Empty cart animation
                    cartContent.innerHTML = `
                        <div class="flex flex-col items-center justify-center py-12 px-4 text-center animate-pulse">
                            <div class="w-24 h-24 bg-gray-100 flex items-center justify-center rounded-full shadow-md">
                                <i class="fas fa-shopping-cart text-gray-400 text-4xl"></i>
                            </div>
                            <h3 class="mt-4 text-lg font-semibold text-gray-700">Your cart is empty</h3>
                            <p class="text-gray-500 text-sm mt-1">Start adding items to see them here.</p>
                            <button 
                                onclick="closeCart()" 
                                class="mt-4 px-4 py-2 bg-shipzoid-teal text-white rounded-lg shadow hover:bg-teal-600 transition">
                                Shop Now
                            </button>
                        </div>
                    `;

                    
                    // Reset totals and hide footer
                    document.getElementById("cart-total").textContent = 0;
                    document.getElementById("cart-count").textContent = 0;
                    cartFooter.classList.add("hidden");
                    return;
                }

                  cartFooter.classList.remove("hidden");

                // Items exist, render them
                cartItems.forEach(item => {
                    total += item.price * item.quantity;

                    const itemDiv = document.createElement("div");
                    itemDiv.className = "grid grid-cols-1 sm:grid-cols-3 items-center gap-4 border rounded-lg p-4 shadow-sm";

                    itemDiv.innerHTML = `
                        <!-- Image -->
                        <div class="flex justify-center sm:justify-start">
                            <img src="${item.image}" alt="${item.name}" class="w-24 h-24 object-cover rounded-lg">
                        </div>

                        <!-- Details -->
                        <div class="flex-1">
                            <h4 class="font-semibold text-lg text-gray-900">${item.name}</h4>
                            ${item.size ? `<p class="text-sm text-gray-600">Size: ${item.size}</p>` : ""}
                            <div class="flex flex-wrap items-center gap-3 mt-2 text-gray-700">
                                <span>Price: ₹${Number(item.price).toFixed(2)}</span>
                                <div class="flex items-center gap-2">
                                    <button class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300" 
                                        onclick="event.stopPropagation(); decreaseQty(${item.id})">-</button>
                                    <span class="px-2">${item.quantity}</span>
                                    <button class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300" 
                                        onclick="event.stopPropagation(); increaseQty(${item.id})">+</button>
                                </div>
                            </div>
                        </div>

                        <!-- Total + Remove -->
                        <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2">
                            <div class="font-semibold text-lg">₹${(item.price * item.quantity).toFixed(0)}</div>
                            <button class="text-red-500 hover:text-red-700" 
                                onclick="event.stopPropagation(); removeFromCart(${item.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `;
                    cartContent.appendChild(itemDiv);
                });

                // Update totals
                const totalItems = cartItems.reduce((acc, item) => acc + item.quantity, 0);
                document.getElementById("cart-total").textContent = total.toFixed(0);

                const cartCountEl = document.getElementById("cart-count");
                if (totalItems > 0) {
                    cartCountEl.classList.remove("hidden");
                    cartCountEl.textContent = totalItems;
                } else {
                    cartCountEl.classList.add("hidden");
                    cartCountEl.textContent = '';
                }

            }


            function updateCartQty(id, quantity) {
                $.ajax({
                    url: `cart/update/${id}/`,
                    method: "POST",
                    data: {
                        quantity: quantity
                    },
                    headers: {
                        "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
                    },
                    success: function (response) {
                        if (response.success) {
                            showSuccess(response.message);
                            fetchCart(); // Refresh cart after update
                        } else {
                            showError(response.message);
                        }
                    },
                    error: function (xhr) {
                        if (xhr.status === 401) {
                            // Unauthorized - prompt user to log in
                            showError("Please login to update your cart.");
                        } else if (xhr.responseJSON && xhr.responseJSON.message) {
                            showError(xhr.responseJSON.message);
                        } else {
                            showError("Failed to update cart quantity.");
                        }
                    }
                });
            }


            // Quantity change functions
            function increaseQty(id) {
                const item = cartItems.find(i => i.id === id);
                if (item) {
                    const newQty = item.quantity + 1;
                    updateCartQty(id, newQty);
                }
            }

            function decreaseQty(id) {
                const item = cartItems.find(i => i.id === id);
                if (item && item.quantity > 1) {
                    const newQty = item.quantity - 1;
                    updateCartQty(id, newQty);
                }
            }


            // Utility to show success toast
            function showSuccess(message) {
                const toast = document.getElementById("success-toast");
                document.getElementById("success-message").textContent = message;

                toast.classList.remove("translate-y-full");
                setTimeout(() => {
                    toast.classList.add("translate-y-full");
                }, 3000); // Hide after 3 seconds
            }

            // Utility to show error toast
            function showError(message) {
                const toast = document.getElementById("error-toast");
                document.getElementById("error-message").textContent = message;

                toast.classList.remove("translate-y-full");
                setTimeout(() => {
                    toast.classList.add("translate-y-full");
                }, 3000); // Hide after 3 seconds
            }

            // Function to remove item from cart
            function removeFromCart(id) {
                $.ajax({
                    url: `/home/cart/remove/${id}`,  // Correct path as per your URL
                    method: "POST",
                    headers: {
                        "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
                    },
                    success: function(response) {
                        if (response.success) {
                            showSuccess(response.message || "Item removed from cart.");
                            fetchCart(); // Refresh cart after removal
                        } else {
                            showError(response.message || "Failed to remove item from cart.");
                        }
                    },
                    error: function(xhr) {
                        if (xhr.status === 401) {
                            showError("Please login to manage your cart.");
                            openLoginModal();
                        } else {
                            showError("An error occurred while removing item from cart.");
                        }
                    }
                });
            }



            // Show/hide cart modal
            const cartModal = document.getElementById("cart-modal");
            const cartBtn = document.getElementById("cart-btn");
            const closeCartBtn = document.getElementById("close-cart-modal");

            cartBtn.addEventListener("click", () => {
                cartModal.classList.remove("hidden", "opacity-0");
                cartModal.classList.add("opacity-100");
                cartModal.querySelector("#cart-modal-content").classList.remove("scale-95");
                cartModal.querySelector("#cart-modal-content").classList.add("scale-100");
                fetchCart();
            });

            closeCartBtn.addEventListener("click", closeCart);
            cartModal.addEventListener("click", e => {
                if (!document.getElementById("cart-modal-content").contains(e.target)) {
                    closeCart();
                }
            });

            function closeCart() {
                cartModal.classList.add("opacity-0");
                cartModal.classList.remove("opacity-100");
                cartModal.querySelector("#cart-modal-content").classList.remove("scale-100");
                cartModal.querySelector("#cart-modal-content").classList.add("scale-95");
                setTimeout(() => cartModal.classList.add("hidden"), 300);
            }



    
            const wishlistModal = document.getElementById("wishlist-modal");
            const wishBtn = document.getElementById("wish-btn");
            const closeWishlistBtn = document.getElementById("close-wishlist-modal");

            wishBtn.addEventListener("click", () => {
                wishlistModal.classList.remove("hidden", "opacity-0");
                wishlistModal.classList.add("opacity-100");
                wishlistModal.querySelector("#wishlist-modal-content").classList.remove("scale-95");
                wishlistModal.querySelector("#wishlist-modal-content").classList.add("scale-100");
                fetchWishlist();
            });

            closeWishlistBtn.addEventListener("click", closeWishlist);

            function closeWishlist() {
                wishlistModal.classList.add("opacity-0");
                wishlistModal.classList.remove("opacity-100");
                wishlistModal.querySelector("#wishlist-modal-content").classList.remove("scale-100");
                wishlistModal.querySelector("#wishlist-modal-content").classList.add("scale-95");
                setTimeout(() => wishlistModal.classList.add("hidden"), 300);
            }


                    // Toast notifications
            function showToast(message, type = 'success') {
                const toast = document.createElement('div');
                toast.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300 ${type === 'success' ? 'bg-green-500' : 'bg-blue-500'} text-white`;
                
                toast.innerHTML = `
                    <div class="flex items-center gap-2">
                        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
                        <span>${message}</span>
                    </div>
                `;
                
                document.body.appendChild(toast);
                
                setTimeout(() => toast.classList.remove('translate-x-full'), 100);
                setTimeout(() => {
                    toast.classList.add('translate-x-full');
                    setTimeout(() => document.body.removeChild(toast), 300);
                }, 3000);
            }

                    document.addEventListener('click', function(event) {
                if (event.target === cartModal) closeCart();
                if (event.target === wishlistModal) closeWishlist();
            });


        let wishlistItems = [];
        async function fetchWishlist() {
            
            try {
                const res = await fetch("/home/wishlist/");

                // Handle if user is not logged in or server returns an error
                if (!res.ok) {
                    const errorData = await res.json();
                    updateWishlistBadge(0); // Reset badge
                    wishlistItems = [];
                    showWishLoginError(errorData.message || "Please login to view your wishlist.");
                    return;
                }

                const data = await res.json();


                // Update wishlist badge
                updateWishlistBadge(data.items?.length || 0);


                // Store and render items
                wishlistItems = data.items || [];
                renderWishlist();

            } catch (error) {
                // console.error("Error fetching wishlist:", error);
                updateWishlistBadge(0);
                wishlistItems = [];
                renderWishlist();

                showError("Failed to load wishlist. Please try again.");
            } finally {
               
            }
        }


            function showWishLoginError(message) {
                const wishContent = document.getElementById("wishlist-content");
                wishContent.innerHTML = `
                    <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
                        <div class="w-24 h-24 bg-gray-100 flex items-center justify-center rounded-full shadow-md">
                            <i class="fas fa-user-lock text-gray-400 text-4xl"></i>
                        </div>
                        <h3 class="mt-4 text-lg font-semibold text-gray-700">${message}</h3>
                    </div>
                `;

            }


        function updateWishlistBadge(count) {
            const wishCountEl = document.getElementById('wish-count');
            if (!wishCountEl) return;

            if (count > 0) {
                wishCountEl.style.display = "flex";
                wishCountEl.textContent = count;
            } else {
                wishCountEl.style.display = "none";
                wishCountEl.textContent = '';
            }
        }



        function renderWishlist() {
            const wishlistContent = document.getElementById('wishlist-content');
            const emptyWishlist = document.getElementById('empty-wishlist');

            if (!wishlistItems.length) {
                wishlistContent.innerHTML = '';
                emptyWishlist.classList.remove('hidden');
                emptyWishlist.classList.add('animate-pulse');
                return;
            }

            emptyWishlist.classList.add('hidden');
            wishlistContent.innerHTML = wishlistItems.map(item => `
                <div class="grid grid-cols-1 sm:grid-cols-3 items-center gap-4 border rounded-lg p-4 shadow-sm hover:shadow-lg transition">
                    <!-- Image -->
                    <div class="flex justify-center sm:justify-start">
                        <img src="${item.image}" alt="${item.name}" class="w-24 h-24 object-cover rounded-lg">
                    </div>

                    <!-- Details -->
                    <div class="flex-1">
                        <h4 class="font-semibold text-lg text-gray-900">${item.name}</h4>
                        <div class="flex items-center gap-2 mt-1">
                            <div class="flex text-yellow-400 text-sm">
                                ${'★'.repeat(Math.floor(item.rating))}${'☆'.repeat(5 - Math.floor(item.rating))}
                            </div>
                            <span class="text-sm text-gray-500">${item.rating}</span>
                        </div>
                        <div class="text-shipzoid-teal font-bold text-lg mt-1">₹${item.price.toFixed(2)}</div>
                    </div>

                    <!-- Actions -->
                    <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2">
                        <button onclick="addToCartFromWishlist(${item.id})"
                                class="bg-shipzoid-teal text-white px-4 py-2 rounded-lg hover:bg-shipzoid-teal-dark transition-colors text-sm flex items-center">
                            <i class="fas fa-cart-plus mr-1"></i>Add to Cart
                        </button>
                        <button onclick="removeFromWishlist(${item.id})"
                                class="text-red-500 hover:text-red-700 text-sm flex items-center">
                            <i class="fas fa-trash mr-1"></i>Remove
                        </button>
                    </div>
                </div>
            `).join('');
        }


        function removeFromWishlist(id) {
        $.ajax({
            url: `/home/wishlist/remove/${id}/`,
            method: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
            success: function (response) {
                showSuccess(response.message);
                fetchWishlist();
            },
            error: function () {
                showError("Failed to remove from wishlist.");
            }
        });
         }

         function addToCartFromWishlist(id) {
            $.ajax({
                url: `/home/wishlist/add-to-cart/${id}/`,
                method: "POST",
                headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
                success: function (response) {
                    if (response.success) {
                        showSuccess(response.message);
                        fetchWishlist();
                        fetchCart();
                    } else {
                        showError(response.message);
                    }
                },
                error: function () {
                    showError("Failed to move item to cart.");
                }
            });
        }




        window.addEventListener("load", function () {
            const loader = document.getElementById("page-loader");
            fetchCart();
            fetchWishlist();
            if (loader) {
            loader.classList.add("opacity-0", "pointer-events-none");
            setTimeout(() => loader.remove(), 500); // Remove from DOM after fade
            }
        });



        function togglePassword(inputId, button) {
            const passwordInput = document.getElementById(inputId);
            const icon = button.querySelector("i");

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");
            } else {
                passwordInput.type = "password";
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");
            }
        }

        function ValidatePhoneNumber(input) {
            // Remove anything that's not a digit
            input.value = input.value.replace(/\D/g, '');

            // Limit to 10 digits
            if (input.value.length > 10) {
                input.value = input.value.slice(0, 10);
            }
        }



        $(document).ready(function () {
            // setup CSRF token for AJAX
            $.ajaxSetup({
                headers: {
                    "X-CSRFToken": $('meta[name="csrf-token"]').attr("content")
                }
            });

            $("#signup-form").on("submit", function (e) {
                e.preventDefault();

                let postUrl = $("#signup-form").data("url");

                let formData = {
                    full_name: $("#signup-name").val(),
                    phone_number: $("#signup-phone").val(),
                    password: $("#signup-password").val(),
                    confirm_password: $("#signup-confirm-password").val(),
                };

                $.ajax({
                    url: postUrl,
                    type: "POST",
                    data: formData,
                    beforeSend: function () {
                        $("#signup-btn")
                            .prop("disabled", true)
                            .html('<span class="animate-pulse">Creating...</span>');
                    },
                    success: function (response) {
                        Swal.fire({
                            icon: "success",
                            title: "🎉 Account Created!",
                            text: response.message,
                            background: "#ecfdf5",
                            color: "#065f46",
                            iconColor: "#10b981",
                            confirmButtonColor: "#10b981",
                            showClass: {
                                popup: "animate__animated animate__fadeInDown animate__faster"
                            },
                            hideClass: {
                                popup: "animate__animated animate__fadeOutUp animate__faster"
                            },
                            timer: 2200,
                            showConfirmButton: false,
                        }).then(() => {
                            // 👉 reset signup form
                            $("#signup-form")[0].reset();

                             switchAuthTab('login');
                        });
                    },
                    error: function (xhr) {
                        let res = xhr.responseJSON;
                        Swal.fire({
                            icon: "error",
                            title: "❌ Oops!",
                            text: res?.message || "Something went wrong",
                            background: "#fef2f2",
                            color: "#991b1b",
                            iconColor: "#ef4444",
                            confirmButtonText: "Try Again",
                            confirmButtonColor: "#ef4444",
                            showClass: {
                                popup: "animate__animated animate__shakeX animate__faster"
                            },
                            hideClass: {
                                popup: "animate__animated animate__fadeOutUp animate__faster"
                            }
                        });
                    },
                    complete: function () {
                        $("#signup-btn").prop("disabled", false).html("Create Account");
                    }
                });
            });
        });


        $(document).ready(function () {
            $("#login-form").on("submit", function (e) {
                e.preventDefault();

                let postUrl = $("#login-form").data("url");

                let phone_number = $("#login-phone").val().trim();
                let password = $("#login-password").val().trim();


                if (!/^\d{10}$/.test(phone_number)) {
                    Swal.fire("Invalid", "Phone number must be exactly 10 digits", "warning");
                    return;
                }
                if (!password) {
                    Swal.fire("Invalid", "Password is required", "warning");
                    return;
                }

                $.ajax({
                    url: postUrl,
                    type: "POST",
                    data: {
                        phone_number: phone_number,
                        password: password,
                    },
                    headers: {
                        "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
                    },
                    beforeSend: function () {
                        $("#login-btn")
                            .prop("disabled", true)
                            .html('<span class="animate-pulse">Signing in...</span>');
                    },
                    success: function (response) {
                        Swal.fire({
                            icon: "success",
                            title: "Login Successful",
                            text: response.message,
                            background: "#ecfdf5",
                            color: "#065f46",
                            iconColor: "#10b981",
                            confirmButtonColor: "#10b981",
                            timer: 2000,
                            showConfirmButton: false,
                        }).then(() => {
                            
                            window.location.reload();
                        });
                    },
                    error: function (xhr) {
                        let res = xhr.responseJSON;
                        Swal.fire({
                            icon: "error",
                            title: "❌ Login Failed",
                            text: res?.message || "Invalid credentials",
                            background: "#fef2f2",
                            color: "#991b1b",
                            iconColor: "#ef4444",
                            confirmButtonText: "Try Again",
                            confirmButtonColor: "#ef4444",
                        });
                    },
                    complete: function () {
                        $("#login-btn").prop("disabled", false).html("Sign In");
                    }
                });
            });
        });


        function confirmLogout() {
            Swal.fire({
                title: "Are you sure?",
                text: "You will be logged out of your account.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#10b981", // green
                cancelButtonColor: "#ef4444", // red
                confirmButtonText: "Yes, Logout",
                cancelButtonText: "Cancel"
            }).then((result) => {
                if (result.isConfirmed) {
                    document.getElementById("logout-form").submit();
                }
            });
        }




        