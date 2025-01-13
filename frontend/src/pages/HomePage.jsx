import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

function HomePage() {
  return (
      <main className="h-full w-full flex-1 py-6 pr-6">
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
        <section className="bg-white shadow rounded-xl p-6 mb-6">
          <CardHeader>
            <CardTitle></CardTitle>
          </CardHeader>
          <CardContent className="flex items-end space-x-4">
            
          </CardContent>
        </section>
        <section className="bg-[#3B82F6] text-white p-6 rounded-xl mb-6">
          <h3 className="text-lg font-semibold"></h3>
          <p className="text-sm"></p>
          <Button variant="outline" className="mt-4 bg-white text-[#3B82F6]">
          </Button>
        </section>
        <section className="grid grid-cols-2 gap-6">
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
                    <td>                      
                    </td>
                    <td></td>
                  </tr>
                </tbody>
              </table>
            </CardContent>
          </Card>
        </section>
      </main>
  );
}

export default HomePage;