import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';

const NewItem = () => {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [subcategories, setSubcategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [formData, setFormData] = useState({
    name: '',
    room: '',
    notes: '',
    budget: '',
    category_id: '',
    subcategory_id: ''
  });

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get('/api/dashboard');
      setCategories(response.data.categories);
    } catch (err) {
      setError('خطا در دریافت دسته‌بندی‌ها');
      console.error('Categories fetch error:', err);
    }
  };

  const fetchSubcategories = async (categoryId) => {
    if (!categoryId) {
      setSubcategories([]);
      return;
    }
    
    try {
      const response = await axios.get(`/api/subcategories/${categoryId}`);
      setSubcategories(response.data.subcategories);
    } catch (err) {
      setError('خطا در دریافت زیردسته‌ها');
      console.error('Subcategories fetch error:', err);
    }
  };

  const handleInputChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    if (name === 'category_id') {
      setFormData(prev => ({ ...prev, subcategory_id: '' }));
      fetchSubcategories(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name.trim()) {
      setError('نام آیتم الزامی است');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/items', formData);
      if (response.data.success) {
        navigate(`/items/${response.data.item.id}`);
      } else {
        setError(response.data.message || 'خطا در ایجاد آیتم');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'خطا در ایجاد آیتم');
      console.error('Create item error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>افزودن آیتم جدید</CardTitle>
          <CardDescription>اطلاعات آیتم جدید را وارد کنید</CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 p-3 bg-destructive/10 border border-destructive/20 rounded-md text-destructive text-sm">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="name">نام آیتم *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                placeholder="مثال: یخچال، تلویزیون، مبل"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="room">اتاق</Label>
              <Input
                id="room"
                value={formData.room}
                onChange={(e) => handleInputChange('room', e.target.value)}
                placeholder="مثال: آشپزخانه، پذیرایی"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="budget">بودجه (تومان)</Label>
              <Input
                id="budget"
                type="number"
                value={formData.budget}
                onChange={(e) => handleInputChange('budget', e.target.value)}
                placeholder="مثال: 5000000"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="category_id">دسته‌بندی</Label>
              <Select 
                value={formData.category_id ? formData.category_id.toString() : 'none'} 
                onValueChange={(value) => handleInputChange('category_id', value === 'none' ? '' : parseInt(value))}
                key={`category-${formData.category_id}`}
              >
                <SelectTrigger className="w-full" dir="rtl">
                  <SelectValue placeholder="انتخاب کنید" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">انتخاب کنید</SelectItem>
                  {categories.map(category => (
                    <SelectItem key={category.id} value={category.id.toString()}>
                      {category.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="subcategory_id">زیردسته</Label>
              <Select 
                value={formData.subcategory_id ? formData.subcategory_id.toString() : 'none'} 
                onValueChange={(value) => handleInputChange('subcategory_id', value === 'none' ? '' : parseInt(value))}
                disabled={!formData.category_id}
                key={`subcategory-${formData.subcategory_id}`}
              >
                <SelectTrigger className="w-full" dir="rtl">
                  <SelectValue placeholder="ابتدا دسته‌بندی را انتخاب کنید"/>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">ابتدا دسته‌بندی را انتخاب کنید</SelectItem>
                  {subcategories.map(subcategory => (
                    <SelectItem key={subcategory.id} value={subcategory.id.toString()}>
                      {subcategory.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">یادداشت</Label>
              <Textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="توضیحات اضافی درباره آیتم..."
                rows={4}
              />
            </div>

            <Separator />

            <div className="flex gap-3 justify-end">
              <Button
                type="button"
                onClick={() => navigate('/')}
                variant="outline"
              >
                لغو
              </Button>
              <Button
                type="submit"
                disabled={loading}
              >
                {loading ? 'در حال ایجاد...' : 'ایجاد آیتم'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default NewItem; 