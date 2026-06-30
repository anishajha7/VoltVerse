// booking.js — Slot selection & booking logic


let selectedSlot = null;
let selectedStationData = null;

async function loadStations() {
  const stations = await getStations();
  const select = document.getElementById('station-select');
  select.innerHTML = '<option value="">-- Choose a station near you --</option>';
  stations.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s.id;
    opt.textContent = `${s.name} (${s.charger_type}) — Rs.${s.price_per_hour}/hr`;
    opt.dataset.info = JSON.stringify(s);
    select.appendChild(opt);
  });
}

function onStationChange() {
  const select = document.getElementById('station-select');
  const selected = select.options[select.selectedIndex];
  const info = document.getElementById('station-info');
  if (!select.value) { info.style.display = 'none'; return; }
  selectedStationData = JSON.parse(selected.dataset.info);
  info.style.display = 'block';
  info.innerHTML = `📍 ${selectedStationData.location} &nbsp;|&nbsp; 🔌 ${selectedStationData.charger_type} Charger &nbsp;|&nbsp; 💰 Rs.${selectedStationData.price_per_hour}/hr`;
  loadSlots();
}

async function loadSlots() {
  const stationId = document.getElementById('station-select').value;
  const date = document.getElementById('date-input').value;
  if (!stationId || !date) return;

  const container = document.getElementById('slots-container');
  container.innerHTML = '<p class="hint-text">Loading slots...</p>';
  selectedSlot = null;
  document.getElementById('booking-summary').style.display = 'none';

  const data = await getAvailableSlots(stationId, date);
  const allSlots = ['09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00'];

  const grid = document.createElement('div');
  grid.className = 'slots-grid';

  allSlots.forEach(slot => {
    const btn = document.createElement('button');
    btn.textContent = slot;
    const isAvailable = data.available && data.available.includes(slot);
    btn.className = isAvailable ? 'slot-btn' : 'slot-btn booked';
    if (isAvailable) {
      btn.onclick = () => selectSlot(slot, btn);
    }
    grid.appendChild(btn);
  });

  container.innerHTML = '<p style="font-size:0.82rem;color:#888;margin-bottom:8px;">🟦 Available &nbsp; ⬜ Booked</p>';
  container.appendChild(grid);
}

function selectSlot(slot, btn) {
  document.querySelectorAll('.slot-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  selectedSlot = slot;
  showSummary();
}

function showSummary() {
  if (!selectedSlot || !selectedStationData) return;
  const date = document.getElementById('date-input').value;
  const duration = 60;
  const total = (selectedStationData.price_per_hour * duration / 60).toFixed(2);

  document.getElementById('summary-content').innerHTML = `
    <div class="summary-row"><span>Station</span><span>${selectedStationData.name}</span></div>
    <div class="summary-row"><span>Date</span><span>${date}</span></div>
    <div class="summary-row"><span>Time</span><span>${selectedSlot}</span></div>
    <div class="summary-row"><span>Duration</span><span>60 mins</span></div>
    <div class="summary-row summary-total"><span>Total</span><span>Rs. ${total}</span></div>
  `;
  document.getElementById('booking-summary').style.display = 'block';
}

async function confirmBooking() {
  const user = getCurrentUser();
  if (!user) { alert('Pehle login karo!'); return; }

  const res = await createBooking({
    user_id: user.id,
    station_id: document.getElementById('station-select').value,
    slot_date: document.getElementById('date-input').value,
    slot_time: selectedSlot,
    vehicle_number: document.getElementById('vehicle-input').value,
    duration_mins: 60
  });

  if (res.success) {
    alert(`✅ Booking confirmed!\nTotal: Rs. ${res.total_price}`);
    window.location.href = 'dashboard.html';
  } else {
    alert('❌ ' + (res.error || 'Booking failed'));
  }
}
