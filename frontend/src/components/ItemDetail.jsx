import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Separator } from '@/components/ui/separator';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, LineChart, Line } from 'recharts';

const ItemDetail = () => {
  const { itemId } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState(null);
  const [options, setOptions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddOptionForm, setShowAddOptionForm] = useState(false);
  const [showEditItemForm, setShowEditItemForm] = useState(false);
  const [editingOptionId, setEditingOptionId] = useState(null);
  const [parsingUrl, setParsingUrl] = useState(false);
  const [optionFormData, setOptionFormData] = useState({
    brand: '',
    model_name: '',
    price: '',
    store: '',
    link: '',
    features: '',
    rating: '',
    warranty_months: '',
    available: true,
    notes: ''
  });
  const [itemFormData, setItemFormData] = useState({
    name: '',
    room: '',
    notes: '',
    budget: '',
    category_id: '',
    subcategory_id: ''
  });

  const fetchItemDetails = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/items/${itemId}`);
      setItem(response.data.item);
      setOptions(response.data.options);
      setError(null);
    } catch (err) {
      setError('خطا در دریافت اطلاعات آیتم');
      console.error('Item fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [itemId]);

  const fetchCategories = useCallback(async () => {
    try {
      const response = await axios.get('/api/categories');
      setCategories(response.data.categories);
    } catch (err) {
      console.error('Categories fetch error:', err);
    }
  }, []);

  useEffect(() => {
    if (itemId) {
      fetchItemDetails();
      fetchCategories();
    }
  }, [itemId, fetchItemDetails, fetchCategories]);

  const handleOptionInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setOptionFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
};

  const handleParseUrl = async () => {
    if (!optionFormData.link) {
      setError('لطفاً یک URL وارد کنید');
      return;
    }

    setParsingUrl(true);
    setError(null);

    try {
      const response = await axios.post('/api/options/parse-url', {
        url: optionFormData.link
      });

      if (response.data.success) {
        // Update form data with parsed information
        setOptionFormData(prev => ({
          ...prev,
          brand: response.data.data.brand || prev.brand,
          model_name: response.data.data.model_name || prev.model_name,
          price: response.data.data.price || prev.price,
          store: response.data.data.store || prev.store,
          features: response.data.data.features || prev.features,
          rating: response.data.data.rating || prev.rating,
          warranty_months: response.data.data.warranty_months || prev.warranty_months
        }));
      } else {
        setError(response.data.message || 'خطا در تجزیه URL');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'خطا در تجزیه URL');
      console.error('URL parsing error:', err);
    } finally {
      setParsingUrl(false);
    }
  };

  const handleItemInputChange = (e) => {
    const { name, value } = e.target;
    setItemFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleItemSelectChange = (name, value) => {
    setItemFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleEditItem = () => {
    setItemFormData({
      name: item.name || '',
      room: item.room || '',
      notes: item.notes || '',
      budget: item.budget || '',
      category_id: item.category_id || '',
      subcategory_id: item.subcategory_id || ''
    });
    setShowEditItemForm(true);
  };

  const handleUpdateItem = async (e) => {
    e.preventDefault();
    
    if (!itemFormData.name) {
      setError('نام آیتم الزامی است');
      return;
    }

    try {
      const response = await axios.put(`/api/items/${itemId}`, itemFormData);
      
      if (response.data.success) {
        await fetchItemDetails();
        setShowEditItemForm(false);
        setError(null);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'خطا در به‌روزرسانی آیتم');
      console.error('Update item error:', err);
    }
  };

  const handleEditOption = (option) => {
    setOptionFormData({
      brand: option.brand || '',
      model_name: option.model_name || '',
      price: option.price || '',
      store: option.store || '',
      link: option.link || '',
      features: option.features || '',
      rating: option.rating || '',
      warranty_months: option.warranty_months || '',
      available: option.available,
      notes: option.notes || ''
    });
    setEditingOptionId(option.id);
  };

  const handleUpdateOption = async (e) => {
    e.preventDefault();

    if (!optionFormData.brand || !optionFormData.model_name) {
      setError('برند و نام مدل الزامی است');
      return;
    }

    try {
      const response = await axios.put(`/api/options/${editingOptionId}`, optionFormData);

      if (response.data.success) {
        await fetchItemDetails();
        setEditingOptionId(null);
        setOptionFormData({
          brand: '',
          model_name: '',
          price: '',
          store: '',
          link: '',
          features: '',
          rating: '',
          warranty_months: '',
          available: true,
          notes: ''
        });
        setError(null);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'خطا در به‌روزرسانی گزینه');
      console.error('Update option error:', err);
    }
  };

  const handleCancelEdit = () => {
    setShowEditItemForm(false);
    setEditingOptionId(null);
    setOptionFormData({
      brand: '',
      model_name: '',
      price: '',
      store: '',
      link: '',
      features: '',
      rating: '',
      warranty_months: '',
      available: true,
      notes: ''
    });
    setError(null);
  };

  const handleAddOption = async (e) => {
    e.preventDefault();

    if (!optionFormData.brand || !optionFormData.model_name) {
      setError('برند و نام مدل الزامی است');
      return;
    }

    try {
      const response = await axios.post('/api/options', {
        ...optionFormData,
        item_id: itemId
      });

      if (response.data.success) {
        setOptions(prev => [...prev, response.data.option]);
        setOptionFormData({
          brand: '',
          model_name: '',
          price: '',
          store: '',
          link: '',
          features: '',
          rating: '',
          warranty_months: '',
          available: true,
          notes: ''
        });
        setShowAddOptionForm(false);
        setError(null);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'خطا در افزودن گزینه');
      console.error('Add option error:', err);
    }
  };

  const handleSelectOption = async (optionId) => {
    try {
      await axios.put(`/api/options/${optionId}/select`);
      fetchItemDetails(); // Refresh to update selection states
    } catch (err) {
      setError('خطا در انتخاب گزینه');
      console.error('Select option error:', err);
    }
  };

  const handleUnselectOption = async (optionId) => {
    try {
      await axios.put(`/api/options/${optionId}/unselect`);
      fetchItemDetails(); // Refresh to update selection states
    } catch (err) {
      setError('خطا در لغو انتخاب گزینه');
      console.error('Unselect option error:', err);
    }
  };

  const handleDeleteOption = async (optionId) => {
    if (window.confirm('آیا مطمئن هستید که می‌خواهید این گزینه را حذف کنید؟')) {
      try {
        await axios.delete(`/api/options/${optionId}`);
        fetchItemDetails(); // Refresh to update options list
      } catch (err) {
        setError('خطا در حذف گزینه');
        console.error('Delete option error:', err);
      }
    }
  };

  const handleDeleteItem = async () => {
    if (window.confirm('آیا مطمئن هستید که می‌خواهید این آیتم را حذف کنید؟')) {
      try {
        await axios.delete(`/api/items/${itemId}`);
        navigate('/');
      } catch (err) {
        setError('خطا در حذف آیتم');
        console.error('Delete item error:', err);
      }
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">در حال بارگذاری...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-destructive">{error}</div>
        </div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">آیتم یافت نشد</div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      {/* Item Header */}
      <Card>
        <CardHeader>
          <div className="flex max-md:flex-col items-center justify-between">
            <div>
              <CardTitle className="text-3xl">{item.name}</CardTitle>
              <CardDescription>جزئیات و گزینه‌های آیتم</CardDescription>
            </div>
            <div className="flex gap-2">
              <Button className="max-md:hidden" onClick={() => navigate('/')} variant="outline">
                بازگشت به داشبورد
              </Button>
              <Button onClick={handleDeleteItem} variant="destructive">
                حذف آیتم
              </Button>
              <Button onClick={handleEditItem} variant="outline">
                ویرایش آیتم
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {showEditItemForm ? (
            <form onSubmit={handleUpdateItem} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">نام آیتم *</Label>
                  <Input
                    id="name"
                    name="name"
                    value={itemFormData.name}
                    onChange={handleItemInputChange}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="room">اتاق</Label>
                  <Input
                    id="room"
                    name="room"
                    value={itemFormData.room}
                    onChange={handleItemInputChange}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="budget">بودجه (تومان)</Label>
                  <Input
                    id="budget"
                    name="budget"
                    type="number"
                    value={itemFormData.budget}
                    onChange={handleItemInputChange}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="category">دسته‌بندی</Label>
                  <Select onValueChange={(value) => handleItemSelectChange('category_id', value)} value={itemFormData.category_id}>
                    <SelectTrigger>
                      <SelectValue placeholder="انتخاب کنید" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map(category => (
                        <SelectItem key={category.id} value={category.id}>{category.name}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="subcategory">زیردسته</Label>
                  <Select onValueChange={(value) => handleItemSelectChange('subcategory_id', value)} value={itemFormData.subcategory_id}>
                    <SelectTrigger>
                      <SelectValue placeholder="انتخاب کنید" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.find(cat => cat.id == itemFormData.category_id)?.subcategories?.map(sub => (
                        <SelectItem key={sub.id} value={sub.id}>{sub.name}</SelectItem>
                      )) || []}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="notes">یادداشت</Label>
                <Textarea
                  id="notes"
                  name="notes"
                  value={itemFormData.notes}
                  onChange={handleItemInputChange}
                  rows={3}
                />
              </div>
              <div className="flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={handleCancelEdit}>
                  لغو
                </Button>
                <Button type="submit">ذخیره تغییرات</Button>
              </div>
            </form>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="space-y-1">
                <Label className="text-sm font-medium text-muted-foreground">دسته‌بندی</Label>
                <p className="text-sm">{item.category || 'تعیین نشده'}</p>
              </div>
              <div className="space-y-1">
                <Label className="text-sm font-medium text-muted-foreground">زیردسته</Label>
                <p className="text-sm">{item.subcategory || 'تعیین نشده'}</p>
              </div>
              <div className="space-y-1">
                <Label className="text-sm font-medium text-muted-foreground">اتاق</Label>
                <p className="text-sm">{item.room || 'تعیین نشده'}</p>
              </div>
              <div className="space-y-1">
                <Label className="text-sm font-medium text-muted-foreground">بودجه</Label>
                <p className="text-sm">{item.budget ? item.budget.toLocaleString() : 'تعیین نشده'} تومان</p>
              </div>
              <div className="space-y-1">
                <Label className="text-sm font-medium text-muted-foreground">وضعیت</Label>
                <Badge variant={item.status === 'selected' ? 'default' : 'secondary'}>
                  {item.status === 'selected' ? 'انتخاب شده' : 'انتخاب نشده'}
                </Badge>
              </div>
              {item.notes && (
                <div className="mt-4 space-y-1">
                  <Label className="text-sm font-medium text-muted-foreground">یادداشت</Label>
                  <p className="text-sm">{item.notes}</p>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Options Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>گزینه‌های موجود</CardTitle>
              <CardDescription>مدیریت گزینه‌های خرید برای این آیتم</CardDescription>
            </div>
            <Button
              onClick={() => setShowAddOptionForm(!showAddOptionForm)}
              variant={showAddOptionForm ? "outline" : "default"}
            >
              {showAddOptionForm ? 'لغو' : 'افزودن گزینه جدید'}
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {showAddOptionForm && (
            <Card className="border-dashed">
              <CardHeader>
                <CardTitle className="text-lg">افزودن گزینه جدید</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleAddOption} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="link">لینک محصول</Label>
                      <div className="flex gap-2">
                        <Input
                          id="link"
                          name="link"
                          type="url"
                          value={optionFormData.link}
                          onChange={handleOptionInputChange}
                          placeholder="https://example.com/product"
                        />
                        <Button
                          type="button"
                          onClick={handleParseUrl}
                          disabled={!optionFormData.link || parsingUrl}
                        >
                          {parsingUrl ? 'در حال تجزیه...' : 'تجزیه'}
                        </Button>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="brand">برند *</Label>
                      <Input
                        id="brand"
                        name="brand"
                        value={optionFormData.brand}
                        onChange={handleOptionInputChange}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="model_name">نام مدل *</Label>
                      <Input
                        id="model_name"
                        name="model_name"
                        value={optionFormData.model_name}
                        onChange={handleOptionInputChange}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="price">قیمت (تومان)</Label>
                      <Input
                        id="price"
                        name="price"
                        type="number"
                        value={optionFormData.price}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="store">فروشگاه</Label>
                      <Input
                        id="store"
                        name="store"
                        value={optionFormData.store}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="rating">امتیاز (1-5)</Label>
                      <Input
                        id="rating"
                        name="rating"
                        type="number"
                        min="1"
                        max="5"
                        value={optionFormData.rating}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="warranty_months">گارانتی (ماه)</Label>
                      <Input
                        id="warranty_months"
                        name="warranty_months"
                        type="number"
                        value={optionFormData.warranty_months}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="flex items-center space-x-2 space-x-reverse">
                        <input
                          type="checkbox"
                          name="available"
                          checked={optionFormData.available}
                          onChange={handleOptionInputChange}
                          className="rounded"
                        />
                        <span>موجود است</span>
                      </Label>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="features">امکانات</Label>
                    <Textarea
                      id="features"
                      name="features"
                      value={optionFormData.features}
                      onChange={handleOptionInputChange}
                      rows={3}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="notes">یادداشت</Label>
                    <Textarea
                      id="notes"
                      name="notes"
                      value={optionFormData.notes}
                      onChange={handleOptionInputChange}
                      rows={3}
                    />
                  </div>
                  <Button type="submit" className="w-full">
                    افزودن گزینه
                  </Button>
                </form>
              </CardContent>
            </Card>
          )}

          {editingOptionId && (
            <Card className="border-dashed">
              <CardHeader>
                <CardTitle className="text-lg">ویرایش گزینه</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleUpdateOption} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="link">لینک محصول</Label>
                      <div className="flex gap-2">
                        <Input
                          id="link"
                          name="link"
                          type="url"
                          value={optionFormData.link}
                          onChange={handleOptionInputChange}
                          placeholder="https://example.com/product"
                        />
                        <Button
                          type="button"
                          onClick={handleParseUrl}
                          disabled={!optionFormData.link || parsingUrl}
                        >
                          {parsingUrl ? 'در حال تجزیه...' : 'تجزیه'}
                        </Button>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="brand">برند *</Label>
                      <Input
                        id="brand"
                        name="brand"
                        value={optionFormData.brand}
                        onChange={handleOptionInputChange}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="model_name">نام مدل *</Label>
                      <Input
                        id="model_name"
                        name="model_name"
                        value={optionFormData.model_name}
                        onChange={handleOptionInputChange}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="price">قیمت (تومان)</Label>
                      <Input
                        id="price"
                        name="price"
                        type="number"
                        value={optionFormData.price}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="store">فروشگاه</Label>
                      <Input
                        id="store"
                        name="store"
                        value={optionFormData.store}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="rating">امتیاز (1-5)</Label>
                      <Input
                        id="rating"
                        name="rating"
                        type="number"
                        min="1"
                        max="5"
                        value={optionFormData.rating}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="warranty_months">گارانتی (ماه)</Label>
                      <Input
                        id="warranty_months"
                        name="warranty_months"
                        type="number"
                        value={optionFormData.warranty_months}
                        onChange={handleOptionInputChange}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="flex items-center space-x-2 space-x-reverse">
                        <input
                          type="checkbox"
                          name="available"
                          checked={optionFormData.available}
                          onChange={handleOptionInputChange}
                          className="rounded"
                        />
                        <span>موجود است</span>
                      </Label>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="features">امکانات</Label>
                    <Textarea
                      id="features"
                      name="features"
                      value={optionFormData.features}
                      onChange={handleOptionInputChange}
                      rows={3}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="notes">یادداشت</Label>
                    <Textarea
                      id="notes"
                      name="notes"
                      value={optionFormData.notes}
                      onChange={handleOptionInputChange}
                      rows={3}
                    />
                  </div>
                  <div className="flex justify-end gap-2">
                    <Button type="button" variant="outline" onClick={() => setEditingOptionId(null)}>
                      لغو
                    </Button>
                    <Button type="submit">ذخیره تغییرات</Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          )}

          <Separator />

          {/* Options List */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {options.map(option => (
              <Card key={option.id} className={`${option.selected ? 'ring-2 ring-primary' : ''}`}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{option.brand} {option.model_name}</CardTitle>
                    <Badge variant={option.selected ? 'default' : 'secondary'}>
                      {option.selected ? 'انتخاب شده' : 'موجود'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="text-sm text-muted-foreground space-y-1">
                    {option.price && (
                      <p><strong>قیمت:</strong> {option.price.toLocaleString()} تومان</p>
                    )}
                    {option.store && (
                      <p><strong>فروشگاه:</strong> {option.store}</p>
                    )}
                    {option.features && (
                      <p><strong>امکانات:</strong> {option.features}</p>
                    )}
                    {option.rating && (
                      <p><strong>امتیاز:</strong> {option.rating}/5</p>
                    )}
                    {option.warranty_months && (
                      <p><strong>گارانتی:</strong> {option.warranty_months} ماه</p>
                    )}
                    {option.notes && (
                      <p><strong>یادداشت:</strong> {option.notes}</p>
                    )}
                  </div>
                  <Separator />
                  <div className="flex flex-wrap gap-2">
                    {option.link && (
                      <Button asChild variant="outline" size="sm">
                        <a href={option.link} target="_blank" rel="noopener noreferrer">
                          مشاهده در فروشگاه
                        </a>
                      </Button>
                    )}
                    {option.selected ? (
                      <Button
                        onClick={() => handleUnselectOption(option.id)}
                        variant="outline"
                        size="sm"
                      >
                        لغو انتخاب
                      </Button>
                    ) : (
                      <Button
                        onClick={() => handleSelectOption(option.id)}
                        size="sm"
                      >
                        انتخاب
                      </Button>
                    )}
                    <Button
                      onClick={() => handleEditOption(option)}
                      variant="outline"
                      size="sm"
                    >
                      ویرایش
                    </Button>
                    <Button
                      onClick={() => handleDeleteOption(option.id)}
                      variant="destructive"
                      size="sm"
                    >
                      حذف
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {options.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <p>هیچ گزینه‌ای برای این آیتم تعریف نشده است.</p>
              <p>برای شروع، یک گزینه جدید اضافه کنید.</p>
            </div>
          )}
        </CardContent>
      </Card>

      
      {/* Charts Section */}
      {options.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>نمودار مقایسه گزینه‌ها</CardTitle>
            <CardDescription>مقایسه بصری قیمت و امتیاز گزینه‌های موجود</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex gap-8">
              {/* Price Comparison Chart */}
              <div className="grow space-y-4">
                <h3 className="text-lg font-semibold">مقایسه قیمت‌ها</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={options.filter(opt => opt.price).map(opt => ({
                    name: `${opt.brand} ${opt.model_name}`,
                    price: opt.price,
                    selected: opt.selected
                  }))}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="name"
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      fontSize={12}
                    />
                    <YAxis
                      label={{ value: 'قیمت (تومان)', angle: -90, position: 'insideLeft' }}
                      tickFormatter={(value) => `${(value / 1000000).toFixed(1)}M`}
                    />
                    <Tooltip
                      formatter={(value) => [value.toLocaleString() + ' تومان', 'قیمت']}
                      labelStyle={{ direction: 'rtl' }}
                    />
                    <Bar
                      dataKey="price"
                      fill="#3b82f6"
                      fillOpacity={0.8}
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Rating Comparison Chart */}
              <div className="grow space-y-4">
                <h3 className="text-lg font-semibold">مقایسه امتیازات</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={options.filter(opt => opt.rating).map(opt => ({
                    name: `${opt.brand} ${opt.model_name}`,
                    rating: opt.rating,
                    selected: opt.selected
                  }))}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="name"
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      fontSize={12}
                    />
                    <YAxis
                      label={{ value: 'امتیاز', angle: -90, position: 'insideLeft' }}
                      domain={[0, 5]}
                      ticks={[1, 2, 3, 4, 5]}
                    />
                    <Tooltip
                      formatter={(value) => [value + '/5', 'امتیاز']}
                      labelStyle={{ direction: 'rtl' }}
                    />
                    <Bar
                      dataKey="rating"
                      fill="#10b981"
                      fillOpacity={0.8}
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Price vs Rating Scatter Plot */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">رابطه قیمت و امتیاز</h3>
              <ResponsiveContainer width="100%" height={300}>
                <ScatterChart data={options.filter(opt => opt.price && opt.rating).map(opt => ({
                  name: `${opt.brand} ${opt.model_name}`,
                  price: opt.price,
                  rating: opt.rating,
                  selected: opt.selected
                }))}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    type="number"
                    dataKey="price"
                    name="قیمت"
                    label={{ value: 'قیمت (تومان)', position: 'insideBottom', offset: -10 }}
                    tickFormatter={(value) => `${(value / 1000000).toFixed(1)}M`}
                  />
                  <YAxis
                    type="number"
                    dataKey="rating"
                    name="امتیاز"
                    label={{ value: 'امتیاز', angle: -90, position: 'insideLeft' }}
                    domain={[0, 5]}
                    ticks={[1, 2, 3, 4, 5]}
                  />
                  <Tooltip
                    formatter={(value, name) => [
                      name === 'price' ? value.toLocaleString() + ' تومان' : value + '/5',
                      name === 'price' ? 'قیمت' : 'امتیاز'
                    ]}
                    labelFormatter={(label) => label}
                    labelStyle={{ direction: 'rtl' }}
                  />
                  <Legend />
                  <Scatter
                    dataKey="rating"
                    fill="#8b5cf6"
                    fillOpacity={0.8}
                    stroke="#6366f1"
                    strokeWidth={2}
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ItemDetail;