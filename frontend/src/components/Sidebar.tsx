import { EnvelopeIcon, HomeIcon } from "@heroicons/react/24/outline";

import { classNames } from "@/utils/className";

const navigation = [
  { name: "Home", href: "/", icon: HomeIcon, current: true },
  { name: "Get in touch", href: "/", icon: EnvelopeIcon, current: false },
];

type SidebarProps = {};

export default function Sidebar({}: SidebarProps) {
  return (
    <nav className="flex-1 h-full flex flex-col justify-center">
      <ul role="list" className="flex-1 flex flex-col gap-y-7">
        <li>
          <ul role="list" className="-mx-2 space-y-1">
            {navigation.map((item) => (
              <li key={item.name}>
                <a
                  href={item.href}
                  className={classNames(
                    item.current
                      ? "bg-gray-800 text-white"
                      : "text-gray-400 hover:text-white hover:bg-gray-800",
                    "group flex gap-x-3 p-2 text-sm font-semibold leading-6 rounded-md"
                  )}
                >
                  <item.icon className="shrink-0 w-6 h-6" aria-hidden="true" />
                  {item.name}
                </a>
              </li>
            ))}
          </ul>
        </li>
      </ul>
    </nav>
  );
}
