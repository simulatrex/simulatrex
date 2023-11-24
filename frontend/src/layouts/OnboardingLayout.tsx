import React, { Fragment, useState } from "react";

import { Menu, Transition } from "@headlessui/react";

type OnboardingLayoutProps = {
  children: React.ReactNode;
};

export default function OnboardingLayout({ children }: OnboardingLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <>
      {/* Menu */}
      <Menu as="div" className="absolute top-6 right-6">
        {({ open }) => (
          <Fragment>
            <Menu.Button className="p-2 text-white bg-black rounded-md">
              Menu ☰
            </Menu.Button>
            <Transition
              show={open}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items
                static
                className="absolute right-0 w-56 mt-2 origin-top-right bg-white rounded-md ring-1 ring-black ring-opacity-5 shadow-lg focus:outline-none"
              >
                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={`${
                          active ? "bg-blue-500 text-white" : "text-gray-900"
                        } block px-4 py-2 text-sm`}
                      >
                        Your Item Here
                      </a>
                    )}
                  </Menu.Item>
                </div>
              </Menu.Items>
            </Transition>
          </Fragment>
        )}
      </Menu>

      <div className="absolute top-6 left-6">
        <img
          className="w-auto h-12"
          src="/assets/logo.png"
          alt="Simulatrex Logo"
        />
      </div>

      <main className="py-10">{children}</main>
    </>
  );
}
