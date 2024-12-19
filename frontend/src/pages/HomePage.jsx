import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Sidebar from "@/components/sidebar/Sidebar";

function HomePage() {
  return (
    <div className="flex h-screen p-8 bg-[#f4f5fa]">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 p-6">
        {/* Header */}
        <header className="flex justify-between items-center mb-6">
          <Input
            type="search"
            placeholder="Search..."
            className="w-1/3 focus:outline-[#3B82F6] pb-2"
          />
        </header>

        {/* Cards */}
        <section className="grid grid-cols-4 gap-6 mb-6">
          {[1, 2, 3, 4].map((_, index) => (
            <Card key={index} className="bg-white shadow rounded-xl">
              <CardContent className="flex flex-col items-center justify-center p-3">
                <CardTitle className="text-sm text-gray-500">
                  Card {index + 1}
                </CardTitle>
                <p className="text-2xl font-semibold text-[#000000]"></p>
              </CardContent>
            </Card>
          ))}
        </section>

        {/* Chart Section */}
        <section className="bg-white shadow rounded-xl p-6 mb-6">
          <CardHeader>
            <CardTitle></CardTitle>
          </CardHeader>
          <CardContent className="flex items-end space-x-4">
            
          </CardContent>
        </section>

        {/* Announcement */}
        <section className="bg-[#3B82F6] text-white p-6 rounded-xl mb-6">
          <h3 className="text-lg font-semibold"></h3>
          <p className="text-sm"></p>
          <Button variant="outline" className="mt-4 bg-white text-[#3B82F6]">
            
          </Button>
        </section>

        {/* Activities and Recent Data */}
        <section className="grid grid-cols-2 gap-6">
          {/* Activities */}
          <Card className="bg-white shadow rounded-xl">
            <CardHeader>
              <CardTitle></CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-4">
                <li className="flex items-center">
                  <Badge
                    variant="outline"
                    className="mr-3 bg-green-100 text-green-600"
                  >
                    
                  </Badge>
                  <p></p>
                </li>
                <li className="flex items-center">
                  <Badge
                    variant="outline"
                    className="mr-3 bg-blue-100 text-blue-600"
                  >
                    
                  </Badge>
                  <p></p>
                </li>
              </ul>
            </CardContent>
          </Card>

          {/* Recent Invoices */}
          <Card className="bg-white shadow rounded-xl">
            <CardHeader>
              <CardTitle> </CardTitle>
            </CardHeader>
            <CardContent>
              <table className="w-full text-left">
                <thead>
                  <tr className="text-gray-500 text-sm border-b">
                    <th></th>
                    <th></th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  <tr className="border-b">
                    <td></td>
                    <td></td>
                  </tr>
                  <tr className="border-b">
                    <td></td>
                    <td></td>
                  </tr>
                </tbody>
              </table>
            </CardContent>
          </Card>
        </section>
      </main>
    </div>
  );
}

export default HomePage;
