/* Experience Builder — vanilla JS port of the Framer React component.
   Mount point: <div class="builder-form-container" data-city="Rio de Janeiro"></div>
   Submits to: https://senderemail.surfinnrio.workers.dev
*/
(function () {
  'use strict';

  const COUNTRIES = [
    { iso: 'BR', name: 'Brazil', flag: '🇧🇷', dialCode: '+55', nationality: 'Brazilian' },
    { iso: 'AR', name: 'Argentina', flag: '🇦🇷', dialCode: '+54', nationality: 'Argentinian' },
    { iso: 'CL', name: 'Chile', flag: '🇨🇱', dialCode: '+56', nationality: 'Chilean' },
    { iso: 'CO', name: 'Colombia', flag: '🇨🇴', dialCode: '+57', nationality: 'Colombian' },
    { iso: 'PE', name: 'Peru', flag: '🇵🇪', dialCode: '+51', nationality: 'Peruvian' },
    { iso: 'UY', name: 'Uruguay', flag: '🇺🇾', dialCode: '+598', nationality: 'Uruguayan' },
    { iso: 'PY', name: 'Paraguay', flag: '🇵🇾', dialCode: '+595', nationality: 'Paraguayan' },
    { iso: 'VE', name: 'Venezuela', flag: '🇻🇪', dialCode: '+58', nationality: 'Venezuelan' },
    { iso: 'EC', name: 'Ecuador', flag: '🇪🇨', dialCode: '+593', nationality: 'Ecuadorian' },
    { iso: 'BO', name: 'Bolivia', flag: '🇧🇴', dialCode: '+591', nationality: 'Bolivian' },
    { iso: 'US', name: 'United States', flag: '🇺🇸', dialCode: '+1', nationality: 'American' },
    { iso: 'CA', name: 'Canada', flag: '🇨🇦', dialCode: '+1', nationality: 'Canadian' },
    { iso: 'MX', name: 'Mexico', flag: '🇲🇽', dialCode: '+52', nationality: 'Mexican' },
    { iso: 'CR', name: 'Costa Rica', flag: '🇨🇷', dialCode: '+506', nationality: 'Costa Rican' },
    { iso: 'PA', name: 'Panama', flag: '🇵🇦', dialCode: '+507', nationality: 'Panamanian' },
    { iso: 'DO', name: 'Dominican Republic', flag: '🇩🇴', dialCode: '+1', nationality: 'Dominican' },
    { iso: 'CU', name: 'Cuba', flag: '🇨🇺', dialCode: '+53', nationality: 'Cuban' },
    { iso: 'PT', name: 'Portugal', flag: '🇵🇹', dialCode: '+351', nationality: 'Portuguese' },
    { iso: 'ES', name: 'Spain', flag: '🇪🇸', dialCode: '+34', nationality: 'Spanish' },
    { iso: 'FR', name: 'France', flag: '🇫🇷', dialCode: '+33', nationality: 'French' },
    { iso: 'BE', name: 'Belgium', flag: '🇧🇪', dialCode: '+32', nationality: 'Belgian' },
    { iso: 'NL', name: 'Netherlands', flag: '🇳🇱', dialCode: '+31', nationality: 'Dutch' },
    { iso: 'LU', name: 'Luxembourg', flag: '🇱🇺', dialCode: '+352', nationality: 'Luxembourgish' },
    { iso: 'MC', name: 'Monaco', flag: '🇲🇨', dialCode: '+377', nationality: 'Monegasque' },
    { iso: 'AD', name: 'Andorra', flag: '🇦🇩', dialCode: '+376', nationality: 'Andorran' },
    { iso: 'DE', name: 'Germany', flag: '🇩🇪', dialCode: '+49', nationality: 'German' },
    { iso: 'CH', name: 'Switzerland', flag: '🇨🇭', dialCode: '+41', nationality: 'Swiss' },
    { iso: 'AT', name: 'Austria', flag: '🇦🇹', dialCode: '+43', nationality: 'Austrian' },
    { iso: 'LI', name: 'Liechtenstein', flag: '🇱🇮', dialCode: '+423', nationality: 'Liechtensteiner' },
    { iso: 'GB', name: 'United Kingdom', flag: '🇬🇧', dialCode: '+44', nationality: 'British' },
    { iso: 'IE', name: 'Ireland', flag: '🇮🇪', dialCode: '+353', nationality: 'Irish' },
    { iso: 'IS', name: 'Iceland', flag: '🇮🇸', dialCode: '+354', nationality: 'Icelander' },
    { iso: 'NO', name: 'Norway', flag: '🇳🇴', dialCode: '+47', nationality: 'Norwegian' },
    { iso: 'SE', name: 'Sweden', flag: '🇸🇪', dialCode: '+46', nationality: 'Swedish' },
    { iso: 'FI', name: 'Finland', flag: '🇫🇮', dialCode: '+358', nationality: 'Finnish' },
    { iso: 'DK', name: 'Denmark', flag: '🇩🇰', dialCode: '+45', nationality: 'Danish' },
    { iso: 'FO', name: 'Faroe Islands', flag: '🇫🇴', dialCode: '+298', nationality: 'Faroese' },
    { iso: 'PL', name: 'Poland', flag: '🇵🇱', dialCode: '+48', nationality: 'Polish' },
    { iso: 'CZ', name: 'Czech Republic', flag: '🇨🇿', dialCode: '+420', nationality: 'Czech' },
    { iso: 'SK', name: 'Slovakia', flag: '🇸🇰', dialCode: '+421', nationality: 'Slovak' },
    { iso: 'HU', name: 'Hungary', flag: '🇭🇺', dialCode: '+36', nationality: 'Hungarian' },
    { iso: 'RO', name: 'Romania', flag: '🇷🇴', dialCode: '+40', nationality: 'Romanian' },
    { iso: 'BG', name: 'Bulgaria', flag: '🇧🇬', dialCode: '+359', nationality: 'Bulgarian' },
    { iso: 'MD', name: 'Moldova', flag: '🇲🇩', dialCode: '+373', nationality: 'Moldovan' },
    { iso: 'UA', name: 'Ukraine', flag: '🇺🇦', dialCode: '+380', nationality: 'Ukrainian' },
    { iso: 'BY', name: 'Belarus', flag: '🇧🇾', dialCode: '+375', nationality: 'Belarusian' },
    { iso: 'RU', name: 'Russia', flag: '🇷🇺', dialCode: '+7', nationality: 'Russian' },
    { iso: 'IT', name: 'Italy', flag: '🇮🇹', dialCode: '+39', nationality: 'Italian' },
    { iso: 'SM', name: 'San Marino', flag: '🇸🇲', dialCode: '+378', nationality: 'Sammarinese' },
    { iso: 'VA', name: 'Vatican City', flag: '🇻🇦', dialCode: '+379', nationality: 'Vatican' },
    { iso: 'MT', name: 'Malta', flag: '🇲🇹', dialCode: '+356', nationality: 'Maltese' },
    { iso: 'GR', name: 'Greece', flag: '🇬🇷', dialCode: '+30', nationality: 'Greek' },
    { iso: 'CY', name: 'Cyprus', flag: '🇨🇾', dialCode: '+357', nationality: 'Cypriot' },
    { iso: 'HR', name: 'Croatia', flag: '🇭🇷', dialCode: '+385', nationality: 'Croatian' },
    { iso: 'SI', name: 'Slovenia', flag: '🇸🇮', dialCode: '+386', nationality: 'Slovenian' },
    { iso: 'BA', name: 'Bosnia and Herzegovina', flag: '🇧🇦', dialCode: '+387', nationality: 'Bosnian / Herzegovinian' },
    { iso: 'RS', name: 'Serbia', flag: '🇷🇸', dialCode: '+381', nationality: 'Serbian' },
    { iso: 'ME', name: 'Montenegro', flag: '🇲🇪', dialCode: '+382', nationality: 'Montenegrin' },
    { iso: 'MK', name: 'North Macedonia', flag: '🇲🇰', dialCode: '+389', nationality: 'Macedonian' },
    { iso: 'AL', name: 'Albania', flag: '🇦🇱', dialCode: '+355', nationality: 'Albanian' },
    { iso: 'XK', name: 'Kosovo', flag: '🇽🇰', dialCode: '+383', nationality: 'Kosovar' },
    { iso: 'JP', name: 'Japan', flag: '🇯🇵', dialCode: '+81', nationality: 'Japanese' },
    { iso: 'KR', name: 'South Korea', flag: '🇰🇷', dialCode: '+82', nationality: 'South Korean' },
    { iso: 'CN', name: 'China', flag: '🇨🇳', dialCode: '+86', nationality: 'Chinese' },
    { iso: 'IN', name: 'India', flag: '🇮🇳', dialCode: '+91', nationality: 'Indian' },
    { iso: 'AU', name: 'Australia', flag: '🇦🇺', dialCode: '+61', nationality: 'Australian' },
    { iso: 'NZ', name: 'New Zealand', flag: '🇳🇿', dialCode: '+64', nationality: 'New Zealander / Kiwi' },
    { iso: 'ZA', name: 'South Africa', flag: '🇿🇦', dialCode: '+27', nationality: 'South African' },
    { iso: 'EG', name: 'Egypt', flag: '🇪🇬', dialCode: '+20', nationality: 'Egyptian' },
    { iso: 'TR', name: 'Turkey', flag: '🇹🇷', dialCode: '+90', nationality: 'Turkish' },
    { iso: 'SA', name: 'Saudi Arabia', flag: '🇸🇦', dialCode: '+966', nationality: 'Saudi / Saudi Arabian' },
    { iso: 'AE', name: 'United Arab Emirates', flag: '🇦🇪', dialCode: '+971', nationality: 'Emirati' },
  ];

  const NATIONALITIES = Array.from(new Set(COUNTRIES.map(c => c.nationality))).sort();
  const getCountry = iso => COUNTRIES.find(c => c.iso === iso) || COUNTRIES[0];
  const formatDate = iso => {
    if (!iso) return '';
    const [y, m, d] = iso.split('-');
    return y && m && d ? `${d}/${m}/${y}` : iso;
  };

  // Escape HTML
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const ROOM_CATEGORIES = ['Without Room', 'Shared', 'Private'];
  const ROOM_TYPES = {
    Shared: ['Mixed Economic', 'Mixed Standard', 'Female Economic', 'Female Standard'],
    Private: ['Shared bathroom', 'Double', 'Sea-View', 'Triple', 'Family'],
  };

  // Packages for the Select-a-package mode (matches the React component 1:1)
  const PACKAGES = {
    'Select a package': null,
    'Package 1 - Surf In Rio': { nights: 3, surfLessons: 4, yogaLessons: 1 },
    'Package 2 - Carioca Ride': {
      nights: 5, surfLessons: 4, yogaLessons: 1, surfSkate: 1,
      videoAnalysis: true, videoAnalysisSessions: 1,
      massage: true, extra_massageCount: 1,
    },
    'Package 3 - Surf Intensive': {
      nights: 7, surfLessons: 8, surfGuide: 1, yogaLessons: 2,
      videoAnalysis: true, videoAnalysisSessions: 1,
      massage: true, extra_massageCount: 1,
      transfer: true, massageType: '',
    },
  };
  const PKG_LABELS = {
    nights: 'Nights', surfLessons: 'Surf Lessons', yogaLessons: 'Yoga Lessons',
    surfSkate: 'Surf-skate', videoAnalysis: 'Video Analysis',
    massage: 'Massage included', transfer: 'Airport transfer',
    surfGuide: 'Surf guide',
  };
  const PKG_DISPLAY = {
    videoAnalysis: { countKey: 'videoAnalysisSessions', unit: 'session(s)' },
    massage: { countKey: 'extra_massageCount', unit: 'massage(s)' },
    yogaLessons: { unit: 'lesson(s)' },
    surfLessons: { unit: 'lesson(s)' },
    surfSkate: { unit: 'session(s)' },
    surfGuide: { unit: 'session(s)' },
    videoAnalysisSessions: { omit: true },
    extra_massageCount: { omit: true },
  };
  function formatPackageValue(key, value, pkg) {
    const cfg = PKG_DISPLAY[key];
    if (cfg) {
      if (cfg.omit) return null;
      if (cfg.countKey) {
        const isOn = value, count = pkg[cfg.countKey];
        return isOn === true && count > 0 ? `${count} ${cfg.unit}` : 'No';
      }
      if (cfg.unit) {
        if (typeof value === 'number') return value > 0 ? `${value} ${cfg.unit}` : 'No';
        if (typeof value === 'boolean') return value ? `Yes (${cfg.unit})` : 'No';
        return String(value);
      }
    }
    return typeof value === 'boolean' ? (value ? 'Yes' : 'No') : String(value);
  }

  const initialData = () => ({
    people: 1,
    surfLessons: 1,
    yogaLessons: 1,
    roomCategory: 'Without Room',
    roomType: '',
    proficiency: 'Beginner',
    breakfast: false,
    unlimitedBoardRental: false,
    checkInDate: '',
    checkOutDate: '',
    fullName: '',
    nationality: '',
    email: '',
    countryISO: 'BR',
    countryDial: '+55',
    contactNumber: '',
    additionalNotes: '',
    surfGuide: 0,
    surfSkate: 0,
    extra_videoAnalysis: false,
    extra_videoAnalysisSessions: 1,
    extra_massageService: false,
    extra_massageCount: 1,
    extra_transferService: false,
    extra_transferType: '',
    extra_hike: false,
    extra_rioCityTour: false,
    extra_cariocaExperience: false,
  });

  const validators = {
    1: data => {
      const errs = [];
      if (data.people < 1) errs.push('Number of people → minimum 1');
      if (!data.proficiency) errs.push('Select level');
      return errs;
    },
    2: data => {
      const errs = [];
      if (!data.roomCategory) errs.push('Select room category');
      if (data.roomCategory !== 'Without Room' && !data.roomType) errs.push('Select room option');
      if (!data.checkInDate) errs.push('Select start date');
      if (!data.checkOutDate) errs.push('Select end date');
      else if (new Date(data.checkOutDate) < new Date(data.checkInDate)) errs.push('Invalid range');
      return errs;
    },
    3: data => {
      const errs = [];
      if (!data.fullName || data.fullName.trim().length < 3) errs.push('Full name must have at least 3 characters');
      if (!data.email) errs.push('Email required');
      else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(data.email)) errs.push('Email format invalid (e.g., example@domain.com)');
      if (!data.contactNumber || !data.contactNumber.trim()) errs.push('Phone number required');
      return errs;
    },
  };

  function validate(step, data) {
    const errs = (validators[step] || (() => []))(data);
    if (errs.length) {
      alert(errs.join('\n'));
      return false;
    }
    return true;
  }

  // Component factory
  function ExperienceBuilder(root, { city = 'Select', storageKey = 'experience_make_v2', endpoint = 'https://senderemail.surfinnrio.workers.dev' } = {}) {
    let data;
    try {
      const cached = localStorage.getItem(storageKey);
      data = cached ? Object.assign(initialData(), JSON.parse(cached)) : initialData();
    } catch { data = initialData(); }
    if (city && city !== 'Select') data.city = city;

    let step = 1;
    let extrasOpen = false;
    let sending = false;
    let confirmation = null;

    const save = () => { try { localStorage.setItem(storageKey, JSON.stringify(data)); } catch {} };
    const up = (k, v) => { data[k] = v; save(); render(); };

    function render() {
      if (step === 4 && confirmation) {
        root.innerHTML = tplConfirmation(confirmation);
        bindConfirmation();
        return;
      }
      const stepHtml = step === 1 ? tplStep1(data, extrasOpen) : step === 2 ? tplStep2(data) : tplStep3(data);
      root.innerHTML = `
        <div class="eb-header">
          <div>
            <div class="eb-title">Create your</div>
            <div class="eb-title">package</div>
          </div>
        </div>
        ${stepHtml}
        <div class="eb-divider"></div>
        <div class="eb-btn-row">
          ${step > 1 ? '<button type="button" class="eb-back" aria-label="Back" data-action="back">&larr;</button>' : ''}
          <button type="button" class="eb-primary" data-action="next"${sending ? ' disabled' : ''}>
            ${sending ? 'Sending…' : step < 3 ? 'Continue' : 'Inquire'}
          </button>
        </div>
      `;
      bindStep();
    }

    /* ============ TEMPLATES ============ */

    function tplCounter(id, label, value, min = 0) {
      return `
        <div class="eb-field">
          <label for="${id}" class="eb-label">${esc(label)}</label>
          <div class="eb-counter" id="${id}">
            <button type="button" class="eb-counter-btn" data-counter="${id}" data-delta="-1" data-min="${min}" aria-label="Decrease ${esc(label)}">&minus;</button>
            <span class="eb-counter-val">${value}</span>
            <button type="button" class="eb-counter-btn" data-counter="${id}" data-delta="1" aria-label="Increase ${esc(label)}">+</button>
          </div>
        </div>`;
    }

    function tplSelect(id, label, placeholder, options, value) {
      const opts = [`<option value="">${esc(placeholder)}</option>`]
        .concat(options.map(o => `<option value="${esc(o)}"${o === value ? ' selected' : ''}>${esc(o)}</option>`))
        .join('');
      return `
        <div class="eb-field">
          ${label ? `<label for="${id}" class="eb-label">${esc(label)}</label>` : ''}
          <div class="eb-select-wrap">
            <select id="${id}" class="eb-select" data-field="${id}">${opts}</select>
            <span class="eb-select-arrow"></span>
          </div>
        </div>`;
    }

    function tplCheckbox(id, label, checked) {
      return `
        <div class="eb-checkbox">
          <input type="checkbox" id="${id}" data-field="${id}"${checked ? ' checked' : ''}>
          <label for="${id}" class="eb-label">${esc(label)}</label>
        </div>`;
    }

    function tplDate(id, label, value, min) {
      return `
        <div class="eb-field">
          <label for="${id}" class="eb-label">${esc(label)}</label>
          <div class="eb-date-wrap">
            <input id="${id}" type="date" class="eb-date" data-field="${id}" value="${esc(value)}"${min ? ` min="${esc(min)}"` : ''}>
            <span class="eb-date-icon" aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#494440" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
            </span>
          </div>
        </div>`;
    }

    function tplStep1(d, open) {
      return `
        ${tplCounter('people', 'Number of people', d.people, 1)}
        ${tplSelect('proficiency', 'Level', 'Select', ['Beginner', 'Intermediate', 'Advanced'], d.proficiency)}
        ${tplCounter('surfLessons', 'Surf lessons', d.surfLessons, 0)}
        ${tplCounter('yogaLessons', 'Yoga lessons', d.yogaLessons, 0)}
        ${tplCheckbox('breakfast', 'Add breakfast', d.breakfast)}
        ${tplCheckbox('unlimitedBoardRental', 'Unlimited board rental', d.unlimitedBoardRental)}
        <div class="eb-extras-link" data-action="toggle-extras">${open ? 'Hide extra activities' : 'Extra activities'}</div>
        ${open ? tplExtras(d) : ''}
      `;
    }

    function tplExtras(d) {
      let html = '<div class="eb-extras-panel">';
      html += tplCheckbox('extra_videoAnalysis', 'Video analysis', d.extra_videoAnalysis);
      if (d.extra_videoAnalysis) html += tplCounter('extra_videoAnalysisSessions', 'Sessions', d.extra_videoAnalysisSessions || 1, 1);
      html += tplCheckbox('extra_massageService', 'Massage', d.extra_massageService);
      if (d.extra_massageService) html += tplCounter('extra_massageCount', 'Massages', d.extra_massageCount || 1, 1);
      html += tplCheckbox('extra_transferService', 'Transfer', d.extra_transferService);
      if (d.extra_transferService) html += tplSelect('extra_transferType', null, 'Transfer type', ['Complete', 'Airport → stay', 'Stay → airport'], d.extra_transferType);
      html += tplCheckbox('extra_hike', 'Hike', d.extra_hike);
      html += tplCheckbox('extra_rioCityTour', 'Rio City Tour', d.extra_rioCityTour);
      html += tplCheckbox('extra_cariocaExperience', 'Carioca Experience', d.extra_cariocaExperience);
      html += tplCounter('surfGuide', 'Surf Guide', d.surfGuide || 0, 0);
      html += tplCounter('surfSkate', 'Surf-Skate', d.surfSkate || 0, 0);
      html += '</div>';
      return html;
    }

    function tplStep2(d) {
      let html = tplSelect('roomCategory', 'Room category', 'Select', ROOM_CATEGORIES, d.roomCategory);
      if (d.roomCategory && d.roomCategory !== 'Without Room' && ROOM_TYPES[d.roomCategory]) {
        html += tplSelect('roomType', 'Room type', 'Select', ROOM_TYPES[d.roomCategory], d.roomType);
      }
      html += tplDate('checkInDate', 'Check-in', d.checkInDate);
      html += tplDate('checkOutDate', 'Check-out', d.checkOutDate, d.checkInDate);
      return html;
    }

    function tplPhoneField(d) {
      const selected = getCountry(d.countryISO || 'BR');
      const opts = [...COUNTRIES]
        .sort((a, b) => a.name.localeCompare(b.name))
        .map(c => `<option value="${c.iso}"${c.iso === selected.iso ? ' selected' : ''}>${c.flag} ${esc(c.name)} (${c.dialCode})</option>`)
        .join('');
      return `
        <div class="eb-field">
          <label for="contactNumber" class="eb-label">Phone</label>
          <div class="eb-phone">
            <div class="eb-select-wrap eb-phone-country">
              <select class="eb-select" data-field="countryISO">${opts}</select>
              <span class="eb-select-arrow"></span>
            </div>
            <input id="contactNumber" class="eb-input" type="tel" inputmode="numeric" placeholder="Enter phone number" value="${esc(d.contactNumber)}" data-field="contactNumber">
          </div>
        </div>`;
    }

    function tplStep3(d) {
      return `
        <div class="eb-field">
          <label for="fullName" class="eb-label">Full name</label>
          <input id="fullName" class="eb-input" placeholder="John Doe" value="${esc(d.fullName)}" data-field="fullName">
        </div>
        ${tplSelect('nationality', 'Nationality', 'Select', NATIONALITIES, d.nationality)}
        <div class="eb-field">
          <label for="email" class="eb-label">Email</label>
          <input id="email" class="eb-input" type="email" placeholder="you@example.com" value="${esc(d.email)}" data-field="email">
        </div>
        ${tplPhoneField(d)}
        <div class="eb-field">
          <label for="additionalNotes" class="eb-label">Observations</label>
          <textarea id="additionalNotes" class="eb-textarea" placeholder="Any further comments?" data-field="additionalNotes">${esc(d.additionalNotes)}</textarea>
        </div>
      `;
    }

    function tplConfirmation(d) {
      const extras = [
        d.extra_videoAnalysis && `Video Analysis (${d.extra_videoAnalysisSessions || 1} session/s)`,
        d.extra_massageService && `Massage (${d.extra_massageCount || 1})`,
        d.extra_transferService && `Transfer (${d.extra_transferType || 'Not specified'})`,
        d.extra_hike && 'Hike',
        d.extra_rioCityTour && 'Rio City Tour',
        d.extra_cariocaExperience && 'Carioca Experience',
        (d.surfGuide || 0) > 0 && `Surf Guide (${d.surfGuide})`,
        (d.surfSkate || 0) > 0 && `Surf-Skate (${d.surfSkate})`,
      ].filter(Boolean);
      const c = getCountry(d.countryISO || 'BR');
      const phone = `${c.dialCode} ${d.contactNumber || ''}`;
      const extrasHtml = extras.length ? `
        <div class="eb-summary">
          <p class="eb-confirm-text"><strong>Extra Activities:</strong><br>
            ${extras.map(x => `&nbsp;&nbsp;• ${esc(x)}<br>`).join('')}
          </p>
        </div>` : '';
      return `
        <div class="eb-confirmation">
          <h2 class="eb-confirm-title">Thank you for your inquiry!</h2>
          <p class="eb-confirm-text">We have received your reservation details. We will contact you shortly to confirm availability and provide payment details. Below is a summary of your request:</p>
          <div class="eb-summary">
            <p class="eb-confirm-text">
              <strong>Name:</strong> ${esc(d.fullName)}<br>
              <strong>Email:</strong> ${esc(d.email)}<br>
              <strong>Phone:</strong> ${esc(phone) || 'Not provided'}
            </p>
          </div>
          <div class="eb-summary">
            <p class="eb-confirm-text">
              <strong>Check-in:</strong> ${esc(formatDate(d.checkInDate))}<br>
              <strong>Check-out:</strong> ${esc(formatDate(d.checkOutDate))}<br>
              <strong>Guests:</strong> ${d.people}<br>
              <strong>Surf Level:</strong> ${esc(d.proficiency)}<br>
              <strong>Accommodation:</strong> ${esc(d.roomCategory)}${d.roomType ? ' - ' + esc(d.roomType) : ''}
            </p>
          </div>
          <div class="eb-summary">
            <p class="eb-confirm-text">
              <strong>Selected Items:</strong><br>
              &nbsp;&nbsp;• ${d.surfLessons} Surf Lesson(s)<br>
              &nbsp;&nbsp;• ${d.yogaLessons} Yoga Lesson(s)<br>
              ${d.breakfast ? '&nbsp;&nbsp;• Breakfast Included<br>' : ''}
              ${d.unlimitedBoardRental ? '&nbsp;&nbsp;• Unlimited Board Rental<br>' : ''}
            </p>
          </div>
          ${extrasHtml}
          ${d.additionalNotes ? `
            <div class="eb-summary">
              <p class="eb-confirm-text"><strong>Observations:</strong><br>${esc(d.additionalNotes)}</p>
            </div>` : ''}
          <button type="button" class="eb-primary eb-reset" data-action="reset">Make a New Inquiry</button>
        </div>`;
    }

    /* ============ BINDINGS ============ */

    function bindStep() {
      // Counter buttons
      root.querySelectorAll('[data-counter]').forEach(btn => {
        btn.addEventListener('click', e => {
          e.stopPropagation();
          const field = btn.dataset.counter;
          const delta = Number(btn.dataset.delta);
          const min = Number(btn.dataset.min || 0);
          up(field, Math.max(min, (Number(data[field]) || 0) + delta));
        });
      });
      // Selects & inputs
      root.querySelectorAll('[data-field]').forEach(el => {
        if (el.type === 'checkbox') {
          el.addEventListener('change', e => { e.stopPropagation(); up(el.dataset.field, el.checked); });
        } else if (el.tagName === 'SELECT') {
          el.addEventListener('change', e => {
            e.stopPropagation();
            const field = el.dataset.field;
            const v = el.value;
            if (field === 'countryISO') {
              const c = getCountry(v);
              data.countryISO = v;
              data.countryDial = c.dialCode;
              save();
              // phone value unchanged, just re-render country label
              return;
            }
            if (field === 'roomCategory') {
              data.roomCategory = v;
              data.roomType = '';
              save();
              render();
              return;
            }
            up(field, v);
          });
        } else {
          el.addEventListener('input', e => {
            e.stopPropagation();
            const field = el.dataset.field;
            let v = el.value;
            if (field === 'contactNumber') v = v.replace(/\D/g, '');
            // don't re-render on every keystroke; just mutate + save
            data[field] = v;
            save();
          });
        }
      });
      // Extras toggle
      root.querySelectorAll('[data-action="toggle-extras"]').forEach(el => {
        el.addEventListener('click', e => {
          e.stopPropagation();
          extrasOpen = !extrasOpen;
          render();
        });
      });
      // Nav buttons
      const back = root.querySelector('[data-action="back"]');
      if (back) back.addEventListener('click', e => { e.stopPropagation(); step -= 1; render(); scrollTop(); });
      const next = root.querySelector('[data-action="next"]');
      if (next) next.addEventListener('click', e => {
        e.stopPropagation();
        if (!validate(step, data)) return;
        if (step < 3) { step += 1; render(); scrollTop(); }
        else { submit(); }
      });
    }

    function bindConfirmation() {
      const reset = root.querySelector('[data-action="reset"]');
      if (reset) reset.addEventListener('click', e => {
        e.stopPropagation();
        data = initialData();
        try { localStorage.removeItem(storageKey); } catch {}
        confirmation = null;
        step = 1;
        render();
      });
    }

    function scrollTop() {
      try { root.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch {}
    }

    async function submit() {
      sending = true; render();
      try {
        const fd = new FormData();
        const toSend = { ...initialData(), ...data };
        const c = getCountry(data.countryISO || 'BR');
        const nationalDigits = (data.contactNumber || '').replace(/\D/g, '');
        const phoneE164 = `${c.dialCode}${nationalDigits}`;
        if (city && city !== 'Select') toSend.city = city;
        Object.entries(toSend).forEach(([k, v]) => fd.append(k, typeof v === 'boolean' ? String(v) : v));
        fd.set('contactNumber', phoneE164);

        const res = await fetch(endpoint, { method: 'POST', body: fd });
        if (!res.ok) {
          const t = await res.text();
          throw new Error(`Server error: ${res.status} - ${t}`);
        }
        confirmation = { ...data };
        step = 4;
      } catch (err) {
        console.error('Form submit failed:', err);
        const msg = (err && /Failed to fetch|NetworkError|CORS/.test(err.message || '')) ?
          'Could not reach the server. Please check your connection and try again.' :
          (err && err.message) || 'An error occurred while submitting the form.';
        alert(msg);
      } finally {
        sending = false;
        render();
      }
    }

    // Stop click propagation on the root so it doesn't bubble to parent
    ['pointerdown', 'touchstart', 'click'].forEach(ev => {
      root.addEventListener(ev, e => e.stopPropagation());
    });

    render();
    return { render, getData: () => ({ ...data }), reset: () => { data = initialData(); save(); step = 1; render(); } };
  }

  /* =================================================================
     SELECT-A-PACKAGE Builder (2nd form — opens from "Or explore our packages")
     Port of the React <MinimalTwoStepForm /> component 1:1.
     ================================================================= */
  function SelectBuilder(root, { city = 'Select', storageKey = 'experience_select_v1', endpoint = 'https://senderemail.surfinnrio.workers.dev' } = {}) {
    const initial = () => ({
      city,
      chosenPackage: 'Select a package',
      people: 1,
      proficiency: 'Beginner',
      roomCategory: 'Shared',
      roomType: '',
      includeBreakfast: false,
      includeUnlimitedBoardRental: false,
      p3TransferIncluded: true,
      extrasOpen: false,
      extra_videoAnalysis: false, extra_videoAnalysisSessions: 1,
      extra_rioCityTour: false, extra_hike: false, extra_cariocaExperience: false,
      extra_massageService: false, extra_massageCount: 1,
      extra_transferService: false, extra_transferType: '',
      extra_surfGuide: 0, extra_surfSkate: 0,
      fullName: '', nationality: '', email: '',
      checkInDate: '', checkOutDate: '',
      countryISO: 'BR', countryDial: '+55', contactNumber: '', additionalNotes: '',
    });

    let d;
    try {
      const c = localStorage.getItem(storageKey);
      d = c ? Object.assign(initial(), JSON.parse(c)) : initial();
    } catch { d = initial(); }
    if (city && city !== 'Select') d.city = city;

    let step = 1;
    let sending = false;
    let errorMessage = '';
    let confirmation = null;

    const save = () => { try { localStorage.setItem(storageKey, JSON.stringify(d)); } catch {} };
    const up = (k, v) => { d[k] = v; save(); };

    function validate() {
      if (step === 1) {
        if (d.chosenPackage === 'Select a package') return 'Please select a package.';
      }
      if (step === 2) {
        if (d.roomCategory !== 'Without room' && !d.roomType) return 'Please select a specific room option.';
      }
      if (step === 3) {
        if (!d.fullName || d.fullName.trim().length < 3) return 'Full name must have at least 3 characters.';
        if (!d.email) return 'Email is required.';
        if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(d.email)) return 'Invalid email format (e.g., example@domain.com).';
        if (!d.checkInDate) return 'Check-in date is required.';
        if (!d.checkOutDate) return 'Check-out date is required.';
        if (new Date(d.checkOutDate) < new Date(d.checkInDate)) return 'Check-out date cannot be before check-in date.';
      }
      return null;
    }

    function tplSectionName() {
      return `<div class="eb-section-name"><span>&#10148;</span> Book</div>`;
    }
    function tplSelect(id, label, opts, value, onChangeField) {
      return `
        <div class="eb-field-left">
          <label for="${id}" class="eb-label-left">${esc(label)}</label>
          <div class="eb-select-wrap">
            <select id="${id}" class="eb-selectbox" data-field="${onChangeField || id}">
              ${opts.map(o => {
                if (typeof o === 'string') return `<option value="${esc(o)}"${o === value ? ' selected' : ''}>${esc(o)}</option>`;
                return `<option value="${esc(o.value)}"${o.value === value ? ' selected' : ''}${o.disabled ? ' disabled' : ''}>${esc(o.label)}</option>`;
              }).join('')}
            </select>
            <span class="eb-select-arrow"></span>
          </div>
        </div>`;
    }
    function tplCounter120(id, label, value, min, onAction) {
      return `
        <div class="eb-field-left">
          <label class="eb-label-left">${esc(label)}</label>
          <div class="eb-counter eb-counter-sm">
            <button type="button" class="eb-counter-btn" data-counter="${id}" data-delta="-1" data-min="${min}" aria-label="Decrease">&#x276E;</button>
            <span class="eb-counter-val">${value}</span>
            <button type="button" class="eb-counter-btn" data-counter="${id}" data-delta="1" aria-label="Increase">&#x276F;</button>
          </div>
        </div>`;
    }
    function tplCheck(id, label, checked) {
      return `
        <div class="eb-checkbox-left">
          <input type="checkbox" id="${id}" data-field="${id}"${checked ? ' checked' : ''}>
          <label for="${id}">${esc(label)}</label>
        </div>`;
    }
    function tplDateField(id, label, value, min) {
      return `
        <div class="eb-field-left">
          <label for="${id}" class="eb-label-left">${esc(label)}</label>
          <div class="eb-date-wrap">
            <div class="eb-date-display">${value ? esc(formatDate(value)) : 'Select date'}</div>
            <input id="${id}" type="date" class="eb-date-native" data-field="${id}" value="${esc(value || '')}"${min ? ` min="${esc(min)}"` : ''}>
          </div>
        </div>`;
    }
    function tplTextInput(id, label, value, placeholder, type) {
      return `
        <div class="eb-field-left">
          <label for="${id}" class="eb-label-left">${esc(label)}</label>
          <input id="${id}" type="${type || 'text'}" class="eb-textinput" value="${esc(value || '')}" placeholder="${esc(placeholder || '')}" data-field="${id}">
        </div>`;
    }
    function tplTextarea(id, label, value, placeholder) {
      return `
        <div class="eb-field-left">
          <label for="${id}" class="eb-label-left">${esc(label)}</label>
          <textarea id="${id}" class="eb-textarea" placeholder="${esc(placeholder || '')}" data-field="${id}">${esc(value || '')}</textarea>
        </div>`;
    }
    function tplPhone(value, iso) {
      const c = getCountry(iso || 'BR');
      const opts = [...COUNTRIES].sort((a,b)=>a.name.localeCompare(b.name))
        .map(cc => `<option value="${cc.iso}"${cc.iso === c.iso ? ' selected' : ''}>${cc.flag} ${esc(cc.name)} (${cc.dialCode})</option>`).join('');
      return `
        <div class="eb-field-left">
          <label class="eb-label-left">Phone</label>
          <div class="eb-phone-row">
            <div class="eb-select-wrap eb-phone-country">
              <select class="eb-selectbox" data-field="countryISO">${opts}</select>
              <span class="eb-select-arrow"></span>
            </div>
            <input class="eb-textinput eb-phone-input" type="tel" inputmode="numeric" value="${esc(value || '')}" placeholder="Enter phone number" data-field="contactNumber">
          </div>
        </div>`;
    }

    function tplPackageDetails() {
      const pkg = PACKAGES[d.chosenPackage];
      if (!pkg) return '';
      // Add virtual transfer flag for Package 3
      const display = d.chosenPackage === 'Package 3 - Surf Intensive' ? { ...pkg, transfer: d.p3TransferIncluded } : pkg;
      const rows = Object.entries(display)
        .filter(([k]) => PKG_LABELS[k])
        .map(([k, v]) => {
          const val = formatPackageValue(k, v, display);
          if (val === null) return '';
          return `<li><span class="eb-pkg-check">&check;</span><strong>${esc(PKG_LABELS[k])}:</strong>&nbsp;${esc(val)}</li>`;
        })
        .join('');
      return `
        <div class="eb-pkg-info">
          <h3 class="eb-pkg-title">${esc(d.chosenPackage)}</h3>
          <ul class="eb-pkg-list">${rows}</ul>
        </div>`;
    }

    function tplStep1() {
      return `
        ${tplSelect('chosenPackage', 'Select a package', Object.keys(PACKAGES), d.chosenPackage)}
        ${d.chosenPackage === 'Package 3 - Surf Intensive' ? `
          ${tplSelect('p3TransferIncluded', 'Included airport transfer',
            [{ value: 'keep', label: 'Keep included transfer' }, { value: 'remove', label: 'Do not include transfer' }],
            d.p3TransferIncluded ? 'keep' : 'remove')}
          <div class="eb-hint">This choice only affects the transfer included in Package 3. You can still add a different transfer in the extras below if you wish.</div>
        ` : ''}
        ${tplSelect('proficiency', 'Surf skill level', ['Beginner', 'Intermediate', 'Advanced'], d.proficiency)}
        ${tplCounter120('people', 'Number of people', d.people, 1)}
        ${tplCheck('includeBreakfast', 'Include Breakfast', d.includeBreakfast)}
        ${tplCheck('includeUnlimitedBoardRental', 'Unlimited Board Rental', d.includeUnlimitedBoardRental)}
        <button type="button" class="eb-extras-toggle" data-action="toggle-extras">${d.extrasOpen ? 'Hide extra activities' : 'Show extra activities'}</button>
        ${d.extrasOpen ? tplExtras() : ''}
        ${tplPackageDetails()}
      `;
    }

    function tplExtras() {
      let html = '<div class="eb-extras-panel">';
      html += tplCheck('extra_videoAnalysis', 'Video analysis', d.extra_videoAnalysis);
      if (d.extra_videoAnalysis) html += `<div class="eb-indent">${tplCounter120('extra_videoAnalysisSessions', 'Sessions', d.extra_videoAnalysisSessions || 1, 1)}</div>`;
      html += tplCheck('extra_massageService', 'Massage', d.extra_massageService);
      if (d.extra_massageService) html += `<div class="eb-indent">${tplCounter120('extra_massageCount', 'Number of Massages', d.extra_massageCount || 1, 1)}</div>`;
      html += tplCheck('extra_transferService', 'Transfer', d.extra_transferService);
      if (d.extra_transferService) html += `<div class="eb-indent">${tplSelect('extra_transferType', 'Transfer type', ['', 'Complete', 'Airport → stay', 'Stay → airport'], d.extra_transferType)}</div>`;
      html += tplCounter120('extra_surfGuide', 'Surf Guide', d.extra_surfGuide || 0, 0);
      html += tplCounter120('extra_surfSkate', 'Surf-skate', d.extra_surfSkate || 0, 0);
      html += '</div>';
      return html;
    }

    function tplStep2() {
      let html = tplSelect('roomCategory', 'Room category', ['Shared', 'Private', 'Without room'], d.roomCategory);
      if (d.roomCategory === 'Shared') {
        html += tplSelect('roomType', 'Shared options', ['', 'Mixed Economic', 'Mixed Standard', 'Female Economic', 'Female Standard'], d.roomType);
      } else if (d.roomCategory === 'Private') {
        html += tplSelect('roomType', 'Private options', ['', 'Shared bathroom', 'Double', 'Sea-View', 'Triple', 'Family'], d.roomType);
      }
      return html;
    }

    function tplStep3() {
      return `
        ${tplTextInput('fullName', 'Full Name', d.fullName, 'Your name')}
        ${tplSelect('nationality', 'Nationality', [{ value: '', label: 'Select nationality', disabled: true }, ...NATIONALITIES], d.nationality)}
        ${tplTextInput('email', 'Email', d.email, 'Email@email.com', 'email')}
        ${tplDateField('checkInDate', 'Check-in Date', d.checkInDate)}
        ${tplDateField('checkOutDate', 'Check-out Date', d.checkOutDate, d.checkInDate)}
        ${tplPhone(d.contactNumber, d.countryISO)}
        ${tplTextarea('additionalNotes', 'Additional Notes', d.additionalNotes, 'Any additional notes or special requests?')}
      `;
    }

    function tplConfirmation() {
      const pkg = PACKAGES[confirmation.chosenPackage];
      const display = confirmation.chosenPackage === 'Package 3 - Surf Intensive' && pkg ? { ...pkg, transfer: confirmation.p3TransferIncluded } : pkg;
      const pkgRows = display ? Object.entries(display).filter(([k]) => PKG_LABELS[k]).map(([k, v]) => {
        const val = formatPackageValue(k, v, display); if (val === null) return '';
        return `<li><span class="eb-pkg-check">&check;</span><strong>${esc(PKG_LABELS[k])}:</strong>&nbsp;${esc(val)}</li>`;
      }).join('') : '';
      const c = getCountry(confirmation.countryISO || 'BR');
      return `
        <h2 class="eb-confirm-title-left">Thank you for your inquiry!</h2>
        <p class="eb-confirm-text-left">You chose the package: <strong>${esc(confirmation.chosenPackage)}</strong></p>
        ${display ? `<div class="eb-pkg-info"><h3 class="eb-pkg-title">${esc(confirmation.chosenPackage)}</h3><ul class="eb-pkg-list">${pkgRows}</ul></div>` : ''}
        <div class="eb-confirm-text-left">
          <strong>People:</strong> ${confirmation.people}<br>
          <strong>Surf level:</strong> ${esc(confirmation.proficiency)}<br>
          <strong>Room:</strong> ${confirmation.roomCategory === 'Without room' ? 'Without room' : `${esc(confirmation.roomCategory)} — ${esc(confirmation.roomType || 'Not selected')}`}<br>
          <strong>Breakfast:</strong> ${confirmation.includeBreakfast ? 'Yes' : 'No'}<br>
          <strong>Unlimited Board Rental:</strong> ${confirmation.includeUnlimitedBoardRental ? 'Yes' : 'No'}<br>
          <strong>Check-in:</strong> ${esc(formatDate(confirmation.checkInDate))}<br>
          <strong>Check-out:</strong> ${esc(formatDate(confirmation.checkOutDate))}<br>
          <strong>Name:</strong> ${esc(confirmation.fullName)}<br>
          <strong>Email:</strong> ${esc(confirmation.email)}<br>
          <strong>Phone:</strong> ${c.dialCode} ${esc(confirmation.contactNumber)}
        </div>
        <button type="button" class="eb-primary" data-action="reset">Make a New Inquiry</button>
      `;
    }

    function render() {
      if (step === 4 && confirmation) {
        root.innerHTML = tplConfirmation();
        bindConfirmation();
        return;
      }
      const stepHtml = step === 1 ? tplStep1() : step === 2 ? tplStep2() : tplStep3();
      root.innerHTML = `
        ${tplSectionName()}
        <div class="eb-header-left">
          <div class="eb-title-right">Select</div>
          <div class="eb-title-right">a package</div>
        </div>
        ${stepHtml}
        ${errorMessage ? `<div class="eb-error">${esc(errorMessage)}</div>` : ''}
        <div class="eb-btn-row">
          ${step > 1 ? '<button type="button" class="eb-back" data-action="back" aria-label="Back">&larr;</button>' : ''}
          <button type="button" class="eb-primary" data-action="next"${sending ? ' disabled' : ''}>
            ${sending ? 'Sending…' : step < 3 ? (step === 2 && d.roomType === '' ? 'Continue without' : 'Continue') : 'Reserve Your Spot'}
          </button>
        </div>
      `;
      bindStep();
    }

    function bindStep() {
      root.querySelectorAll('[data-counter]').forEach(btn => {
        btn.addEventListener('click', e => {
          e.stopPropagation();
          const field = btn.dataset.counter;
          const delta = Number(btn.dataset.delta);
          const min = Number(btn.dataset.min || 0);
          d[field] = Math.max(min, (Number(d[field]) || 0) + delta);
          save(); render();
        });
      });
      root.querySelectorAll('[data-field]').forEach(el => {
        if (el.type === 'checkbox') {
          el.addEventListener('change', e => { e.stopPropagation(); up(el.dataset.field, el.checked); render(); });
        } else if (el.tagName === 'SELECT') {
          el.addEventListener('change', e => {
            e.stopPropagation();
            const field = el.dataset.field;
            const v = el.value;
            if (field === 'countryISO') {
              const c = getCountry(v);
              d.countryISO = v; d.countryDial = c.dialCode; save();
              return;
            }
            if (field === 'roomCategory') { d.roomCategory = v; d.roomType = ''; save(); render(); return; }
            if (field === 'chosenPackage') { d.chosenPackage = v; save(); render(); return; }
            if (field === 'p3TransferIncluded') { d.p3TransferIncluded = (v === 'keep'); save(); render(); return; }
            up(field, v); render();
          });
        } else {
          el.addEventListener('input', e => {
            e.stopPropagation();
            const field = el.dataset.field;
            let v = el.value;
            if (field === 'contactNumber') v = v.replace(/\D/g, '');
            d[field] = v; save();
          });
          if (el.type === 'date') {
            el.addEventListener('change', e => { e.stopPropagation(); d[el.dataset.field] = el.value; save(); render(); });
          }
        }
      });
      const extrasToggle = root.querySelector('[data-action="toggle-extras"]');
      if (extrasToggle) extrasToggle.addEventListener('click', e => { e.stopPropagation(); d.extrasOpen = !d.extrasOpen; save(); render(); });
      const back = root.querySelector('[data-action="back"]');
      if (back) back.addEventListener('click', e => { e.stopPropagation(); step -= 1; errorMessage = ''; render(); root.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
      const next = root.querySelector('[data-action="next"]');
      if (next) next.addEventListener('click', e => {
        e.stopPropagation();
        const err = validate();
        if (err) { errorMessage = err; render(); return; }
        errorMessage = '';
        if (step < 3) { step += 1; render(); root.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        else submit();
      });
    }

    function bindConfirmation() {
      const btn = root.querySelector('[data-action="reset"]');
      if (btn) btn.addEventListener('click', e => {
        e.stopPropagation();
        d = initial();
        try { localStorage.removeItem(storageKey); } catch {}
        confirmation = null; step = 1; render();
      });
    }

    async function submit() {
      sending = true; render();
      try {
        const fd = new FormData();
        fd.append('city', d.city || 'Select');
        fd.append('package', d.chosenPackage);
        fd.append('people', String(d.people));
        fd.append('proficiency', d.proficiency);
        fd.append('roomCategory', d.roomCategory);
        fd.append('roomType', d.roomType);
        fd.append('breakfast', String(d.includeBreakfast));
        fd.append('unlimitedBoardRental', String(d.includeUnlimitedBoardRental));
        fd.append('extra_videoAnalysis', String(d.extra_videoAnalysis));
        if (d.extra_videoAnalysis) fd.append('extra_videoAnalysisSessions', String(d.extra_videoAnalysisSessions));
        fd.append('extra_rioCityTour', String(d.extra_rioCityTour));
        fd.append('extra_hike', String(d.extra_hike));
        fd.append('extra_cariocaExperience', String(d.extra_cariocaExperience));
        fd.append('extra_massageService', String(d.extra_massageService));
        if (d.extra_massageService) fd.append('extra_massageCount', String(d.extra_massageCount));
        fd.append('extra_transferService', String(d.extra_transferService));
        if (d.extra_transferService) fd.append('extra_transferType', d.extra_transferType);

        const pkg = PACKAGES[d.chosenPackage];
        if (pkg) Object.entries(pkg).forEach(([k, v]) => fd.append(k, String(v)));
        if (d.chosenPackage === 'Package 3 - Surf Intensive') fd.set('transfer', String(!!d.p3TransferIncluded));
        const baseGuide = (pkg && Number(pkg.surfGuide)) || 0;
        const baseSkate = (pkg && Number(pkg.surfSkate)) || 0;
        fd.set('surfGuide', String(baseGuide + Number(d.extra_surfGuide || 0)));
        fd.set('surfSkate', String(baseSkate + Number(d.extra_surfSkate || 0)));

        fd.append('fullName', d.fullName);
        fd.append('nationality', d.nationality);
        fd.append('email', d.email);
        fd.append('checkInDate', d.checkInDate);
        fd.append('checkOutDate', d.checkOutDate);
        fd.append('additionalNotes', d.additionalNotes);
        const c = getCountry(d.countryISO || 'BR');
        const nationalDigits = (d.contactNumber || '').replace(/\D/g, '');
        fd.set('contactNumber', `${c.dialCode}${nationalDigits}`);

        const resp = await fetch(endpoint, { method: 'POST', body: fd });
        if (!resp.ok) throw new Error(await resp.text());
        confirmation = { ...d };
        step = 4;
      } catch (err) {
        console.error(err);
        errorMessage = `Error: ${err.message || 'Could not send. Try again.'}`;
      } finally {
        sending = false; render();
      }
    }

    // Prevent click bubbling to parent
    ['pointerdown', 'touchstart', 'click'].forEach(ev => root.addEventListener(ev, e => e.stopPropagation()));

    render();
    return { render };
  }

  // Auto-mount every element matching .builder-form-container
  function mount() {
    document.querySelectorAll('.builder-form-container').forEach(el => {
      if (el.dataset.mounted) return;
      el.dataset.mounted = '1';
      const mode = el.dataset.mode || 'create';
      const opts = {
        city: el.dataset.city || 'Select',
        storageKey: el.dataset.storageKey || (mode === 'select' ? 'experience_select_v1' : 'experience_make_v2'),
        endpoint: el.dataset.endpoint || 'https://senderemail.surfinnrio.workers.dev',
      };
      if (mode === 'select') SelectBuilder(el, opts);
      else ExperienceBuilder(el, opts);
    });
  }

  // Toggle between Create / Select forms in the same section
  function wireToggles() {
    document.querySelectorAll('.builder').forEach(section => {
      if (section.dataset.toggleBound) return;
      section.dataset.toggleBound = '1';
      const slot = section.querySelector('.builder-form-slot');
      if (!slot) return;
      const forms = {
        create: slot.querySelector('[data-mode="create"]'),
        select: slot.querySelector('[data-mode="select"]'),
      };
      const images = {
        create: section.querySelector('.builder-image[data-for-mode="create"]'),
        select: section.querySelector('.builder-image[data-for-mode="select"]'),
      };
      const btns = {
        create: section.querySelector('[data-switch="create"]'),
        select: section.querySelector('[data-switch="select"]'),
      };
      function show(which) {
        if (!forms[which]) return;
        section.dataset.activeMode = which;
        if (forms.create) forms.create.hidden = which !== 'create';
        if (forms.select) forms.select.hidden = which !== 'select';
        if (images.create) images.create.hidden = which !== 'create';
        if (images.select) images.select.hidden = which !== 'select';
      }
      if (btns.select) btns.select.addEventListener('click', e => { e.preventDefault(); show('select'); });
      if (btns.create) btns.create.addEventListener('click', e => { e.preventDefault(); show('create'); });
      show('create');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { mount(); wireToggles(); });
  } else {
    mount();
    wireToggles();
  }

  window.ExperienceBuilder = ExperienceBuilder;
})();
