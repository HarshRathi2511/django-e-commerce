from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.base import View
from cart.models import OrderItem, Order
from user.models import Address
from .models import Category, Product
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

