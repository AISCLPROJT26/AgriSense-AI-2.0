// ==========================================
// AGRISENSE AI 2.0 - MAIN JAVASCRIPT LOGIC
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // --------------------------------------
    // 1. ONLINE INTERACTIVE GIS MAP (OSM + SATELLITE)
    // --------------------------------------
    const mapElement = document.getElementById("farmMap");
    if (mapElement && typeof L !== "undefined") {
        // Centered on Meerut Agricultural Region
        const map = L.map("farmMap").setView([28.9845, 77.7064], 14);

        const streetLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "© OpenStreetMap contributors",
            maxZoom: 19
        });

        const satelliteLayer = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
            attribution: "© Esri World Imagery",
            maxZoom: 19
        });

        // Load Satellite View by default for farmland inspection
        satelliteLayer.addTo(map);
        L.control.layers({
            "Satellite View": satelliteLayer,
            "Street Map": streetLayer
        }).addTo(map);

        // Field Polygons
        L.polygon([[28.988, 77.701], [28.992, 77.704], [28.989, 77.708]], {
            color: "#198754", fillColor: "#198754", fillOpacity: 0.45
        }).addTo(map).bindPopup("<b>Field A: Wheat</b><br>Moisture: 68% (Optimal)<br>Status: Healthy");

        L.polygon([[28.983, 77.706], [28.986, 77.710], [28.981, 77.712]], {
            color: "#ffc107", fillColor: "#ffc107", fillOpacity: 0.45
        }).addTo(map).bindPopup("<b>Field B: Mustard</b><br>Moisture: 38% (Irrigate Soon)");

        L.polygon([[28.978, 77.700], [28.981, 77.705], [28.976, 77.707]], {
            color: "#dc3545", fillColor: "#dc3545", fillOpacity: 0.45
        }).addTo(map).bindPopup("<b>Field C: Potato</b><br>Alert: High Humidity — Check for Blight");

        // Live GPS "My Location" Button
        const locateBtn = document.getElementById("locateFarmBtn");
        if (locateBtn) {
            locateBtn.innerHTML = '<i class="fa-solid fa-crosshairs me-1"></i> My Location';
            locateBtn.addEventListener("click", () => {
                if (!navigator.geolocation) {
                    alert("Geolocation is not supported by your browser.");
                    return;
                }
                locateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Locating...';
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        const { latitude, longitude } = pos.coords;
                        map.setView([latitude, longitude], 16);
                        L.marker([latitude, longitude]).addTo(map)
                            .bindPopup("<b>Your Live Farm GPS Location</b>").openPopup();
                        locateBtn.innerHTML = '<i class="fa-solid fa-check me-1"></i> Located';
                    },
                    () => {
                        alert("Unable to retrieve GPS location. Please allow browser location access.");
                        locateBtn.innerHTML = '<i class="fa-solid fa-crosshairs me-1"></i> My Location';
                    }
                );
            });
        }
    }

    // --------------------------------------
    // 2. OFFLINE DAILY MANDI CROP PRICES (FROM SQLITE)
    // --------------------------------------
    const priceBody = document.getElementById("marketPriceBody");
    const ticker = document.getElementById("priceTicker");
    const searchInput = document.getElementById("cropSearchInput");
    let allPrices = [];

    function renderPrices(list) {
        if (!priceBody) return;
        if (list.length === 0) {
            priceBody.innerHTML = '<tr><td colspan="4" class="text-center py-3 text-muted">No matching crops found.</td></tr>';
            return;
        }
        priceBody.innerHTML = list.map(item => {
            const badgeClass = item.trend === "up" ? "bg-success" : (item.trend === "down" ? "bg-danger" : "bg-secondary");
            const icon = item.trend === "up" ? "fa-arrow-trend-up" : (item.trend === "down" ? "fa-arrow-trend-down" : "fa-minus");
            return `
                <tr>
                    <td class="fw-bold text-dark">${item.crop}</td>
                    <td class="text-muted">${item.mandi}</td>
                    <td class="fw-bold text-success">₹${item.modal_price} <small class="text-muted fw-normal">/ qtl</small></td>
                    <td><span class="badge ${badgeClass} bg-opacity-75"><i class="fa-solid ${icon} me-1"></i>${item.change}</span></td>
                </tr>
            `;
        }).join("");
    }

    if (priceBody) {
        fetch("/api/market-prices")
            .then(res => res.json())
            .then(data => {
                allPrices = data.prices || [];
                renderPrices(allPrices);

                const label = document.getElementById("marketSourceLabel");
                if (label && data.source) label.innerText = `${data.source} • ₹ per Quintal (100 kg)`;

                if (ticker && allPrices.length > 0) {
                    ticker.innerHTML = allPrices.map(p =>
                        `<span class="me-4"><strong>${p.crop}:</strong> ₹${p.modal_price}/qtl (${p.mandi})</span>`
                    ).join(" • ");
                }
            });
    }

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = allPrices.filter(p =>
                p.crop.toLowerCase().includes(term) || p.mandi.toLowerCase().includes(term)
            );
            renderPrices(filtered);
        });
    }
});