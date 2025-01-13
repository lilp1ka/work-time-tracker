import React, { useRef } from "react";
import { Input } from "@/components/ui/input";
import { IoSearchOutline } from "react-icons/io5";

const Search = ({ placeholder, value, onChange }) => {
  const inputRef = useRef(null);

  const handleIconClick = () => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <div className="relative w-full md:w-1/3">
      {/* Іконка в полі вводу */}
      <IoSearchOutline
        className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 cursor-pointer"
        onClick={handleIconClick}
      />
      <Input
        ref={inputRef} // додаємо реф
        type="Search"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="w-full pl-10 focus:outline-[#3B82F6] py-2"
      />
    </div>
  );
};

export default Search;
