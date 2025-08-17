import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const Header = () => {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">خانه خرید</h1>
        <nav className="flex items-center space-x-4 space-x-reverse">
          <Button asChild variant="ghost">
            <Link to="/">داشبورد</Link>
          </Button>
          <Button asChild>
            <Link to="/items/new">افزودن آیتم جدید</Link>
          </Button>
        </nav>
      </div>
    </header>
  );
};

export default Header; 