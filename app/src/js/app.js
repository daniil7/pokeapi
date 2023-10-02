import '../css/app.css';

import Alpine from 'alpinejs'
window.Alpine = Alpine

import Pagination from './pagination.js';
window.Pagination = Pagination;

import API from './api.js'
window.API = API

import './utilities.js'

Alpine.start()
