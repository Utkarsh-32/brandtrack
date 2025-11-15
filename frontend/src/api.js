import axios from "axios";

const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const createBrand = (name) => 
    axios.post(`${BASE}/api/brands`, { name });

export const getSummary = (brand) => 
    axios.get(`${BASE}/api/summary/?brand=${encodeURIComponent(brand)}`);

export const getMentions = (brand) => 
    axios.get(`${BASE}/api/mentions/?brand=${encodeURIComponent(brand)}`);