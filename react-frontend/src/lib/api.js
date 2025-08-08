// src/lib/api.js
import axios from 'axios';
import Cookies from 'js-cookie';
import { supabase } from './supabaseClient';

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // your backend base
  withCredentials: false, // using Bearer header, not cookies
});

api.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  } else {
    const guestId = Cookies.get('guest_id'); // set this when user taps "Start Planning"
    if (guestId) config.headers['X-Guest-Id'] = guestId;
  }
  return config;
});
