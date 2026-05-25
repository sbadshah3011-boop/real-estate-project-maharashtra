import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Title/Header changes
html = html.replace('Pune Estate', 'Maharashtra Estate')
html = html.replace('Pune Real Estate', 'Maharashtra Real Estate')
html = html.replace('Pune Realty', 'Maharashtra Realty')
html = html.replace('Pune localities', 'Maharashtra localities')
html = html.replace('Baner, Wakad, Hinjewadi', 'Bandra, Hinjewadi, Wardha')

# 2. Add city-filter to toolbar
toolbar_search = '''<input type="text" id="market-search" placeholder="Search micro-markets (e.g., Bandra, Hinjewadi, Wardha)..." oninput="filterMarkets()"/>
      </div>'''
toolbar_replace = '''<input type="text" id="market-search" placeholder="Search micro-markets (e.g., Bandra, Hinjewadi, Wardha)..." oninput="filterMarkets()"/>
      </div>
      <select class="filter-select" id="city-filter" onchange="filterMarkets()">
        <option value="all">City: All Maharashtra</option>
        <option value="mumbai">Mumbai</option>
        <option value="pune">Pune</option>
        <option value="nagpur">Nagpur</option>
        <option value="nashik">Nashik</option>
        <option value="thane">Thane</option>
        <option value="navi mumbai">Navi Mumbai</option>
        <option value="aurangabad">Aurangabad</option>
        <option value="kolhapur">Kolhapur</option>
      </select>'''
html = html.replace(toolbar_search, toolbar_replace)

# 3. Add CITY column to table
th_search = '''<th onclick="sortTable(0)" class="sorted">LOCALITY'''
th_replace = '''<th onclick="sortTable(-1)">CITY <span class="sort-arrow"> </span></th>
            <th onclick="sortTable(0)" class="sorted">LOCALITY'''
html = html.replace(th_search, th_replace)

# 4. Update fetchLiveData map
fetch_search = '''allMarkets = data.markets.map(m => ({
        locality: m.locality, profile: m.profile,'''
fetch_replace = '''allMarkets = data.markets.map(m => ({
        city: m.city || 'Unknown',
        locality: m.locality, profile: m.profile,'''
html = html.replace(fetch_search, fetch_replace)

# 5. Update renderMarkets filtering
filter_search = '''const f = document.getElementById('appr-filter').value;
  let data = allMarkets.filter(m => {'''
filter_replace = '''const f = document.getElementById('appr-filter').value;
  const c = document.getElementById('city-filter') ? document.getElementById('city-filter').value : 'all';
  let data = allMarkets.filter(m => {
    const matchC = c === 'all' || (m.city && m.city.toLowerCase() === c);'''
html = html.replace(filter_search, filter_replace)

matchQ_search = '''return matchQ && matchF;'''
matchQ_replace = '''return matchC && matchQ && matchF;'''
html = html.replace(matchQ_search, matchQ_replace)

# 6. Update table rows
row_search = '''<tr>
      <td class="td-locality">${m.locality}</td>'''
row_replace = '''<tr>
      <td style="color:#94a3b8">${m.city || ''}</td>
      <td class="td-locality">${m.locality}</td>'''
html = html.replace(row_search, row_replace)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Dashboard updated')
