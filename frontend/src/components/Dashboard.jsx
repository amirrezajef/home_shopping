import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedSubcategory, setSelectedSubcategory] = useState('all');

  useEffect(() => {
    fetchDashboardData();
  }, [selectedCategory, selectedSubcategory]);

  useEffect(() => {
    if (selectedCategory === 'all') {
      setSelectedSubcategory('all');
    }
  }, [selectedCategory]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const params = {};
      if (selectedCategory && selectedCategory !== 'all') params.category = selectedCategory;
      if (selectedSubcategory && selectedSubcategory !== 'all') params.subcategory = selectedSubcategory;
      
      const response = await axios.get('/api/dashboard', { params });
      setDashboardData(response.data);
      setError(null);
    } catch (err) {
      setError('خطا در دریافت اطلاعات داشبورد');
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = (value) => {
    setSelectedCategory(value);
    setSelectedSubcategory('all');
  };

  const handleSubcategoryChange = (value) => {
    setSelectedSubcategory(value);
  };

  const handleDeleteItem = async (itemId) => {
    if (window.confirm('آیا مطمئن هستید که می‌خواهید این آیتم را حذف کنید؟')) {
      try {
        await axios.delete(`/api/items/${itemId}`);
        fetchDashboardData(); // Refresh data
      } catch (err) {
        setError('خطا در حذف آیتم');
        console.error('Delete error:', err);
      }
    }
  };

  // Helper function to get all items from all categories
  const getAllItems = () => {
    if (!dashboardData?.items_by_category) return [];
    
    // Extract all items from all categories
    const allItems = [];
    Object.values(dashboardData.items_by_category).forEach(categoryItems => {
      if (Array.isArray(categoryItems)) {
        allItems.push(...categoryItems);
      }
    });

    return allItems;
  };

  // Helper function to get items for a specific category
  const getItemsForCategory = (categoryName) => {
    if (!dashboardData?.items_by_category || !categoryName || categoryName === 'all') {
      return getAllItems();
    }
    return dashboardData.items_by_category[categoryName] || [];
  };

  // Helper function to get subcategories for a selected category
  const getSubcategoriesForCategory = (categoryName) => {
    if (!dashboardData?.subcategories || !categoryName) return [];
    return dashboardData.subcategories[categoryName] || [];
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

  if (!dashboardData) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">داده‌ای یافت نشد</div>
        </div>
      </div>
    );
  }

  const allItems = getAllItems();
  const filteredItems = getItemsForCategory(selectedCategory);

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل آیتم‌ها</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardData.total_items || 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">آیتم‌های انتخاب شده</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardData.items_with_choice || 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">درصد تکمیل</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardData.completion || 0}%</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">هزینه کل انتخاب‌ها</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(dashboardData.total_selected_cost || 0).toLocaleString()} تومان</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">بودجه کل</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(dashboardData.total_budget || 0).toLocaleString()} تومان</div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>فیلترها</CardTitle>
          <CardDescription>فیلتر کردن آیتم‌ها بر اساس دسته‌بندی</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <label className="text-sm font-medium mb-2 block">دسته‌بندی</label>
              <Select value={selectedCategory} onValueChange={handleCategoryChange}>
                <SelectTrigger>
                  <SelectValue placeholder="همه دسته‌ها" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">همه دسته‌ها</SelectItem>
                  {dashboardData.categories?.map(cat => (
                    <SelectItem key={cat.id} value={cat.name}>{cat.name}</SelectItem>
                  )) || []}
                </SelectContent>
              </Select>
            </div>
            <div className="flex-1">
              <label className="text-sm font-medium mb-2 block">زیردسته</label>
              <Select value={selectedSubcategory} onValueChange={handleSubcategoryChange} disabled={!selectedCategory || selectedCategory === 'all'}>
                <SelectTrigger>
                  <SelectValue placeholder="همه زیردسته‌ها" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">همه زیردسته‌ها</SelectItem>
                  {selectedCategory && selectedCategory !== 'all' && getSubcategoriesForCategory(selectedCategory).map(subcat => (
                    <SelectItem key={subcat} value={subcat}>{subcat}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Items List */}
      <Card>
        <CardHeader>
          <CardTitle>لیست آیتم‌ها</CardTitle>
          <CardDescription>مدیریت و مشاهده آیتم‌های موجود</CardDescription>
        </CardHeader>
        <CardContent>
          {filteredItems.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              آیتمی یافت نشد
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredItems.map(item => (
                <Card key={item.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{item.name}</CardTitle>
                      <Badge variant={item.selected_option ? 'default' : 'secondary'}>
                        {item.selected_option ? 'انتخاب شده' : 'انتخاب نشده'}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="text-sm text-muted-foreground">
                      <p><strong>دسته:</strong> {item.category || item.room || 'نامشخص'}</p>
                      <p><strong>زیردسته:</strong> {item.subcategory || 'نامشخص'}</p>
                      <p><strong>اتاق:</strong> {item.room || 'نامشخص'}</p>
                      <p><strong>بودجه:</strong> {(item.budget || 0).toLocaleString()} تومان</p>
                      <p><strong>تعداد گزینه‌ها:</strong> {item.options_count || 0}</p>
                      {item.selected_option && (
                        <p><strong>انتخاب:</strong> {item.selected_option.brand} {item.selected_option.model_name}</p>
                      )}
                    </div>
                    <Separator />
                    <div className="flex gap-2">
                      <Button asChild size="sm" className="flex-1">
                        <Link to={`/items/${item.id}`}>
                          مشاهده جزئیات
                        </Link>
                      </Button>
                      <Button 
                        onClick={() => handleDeleteItem(item.id)} 
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
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard; 